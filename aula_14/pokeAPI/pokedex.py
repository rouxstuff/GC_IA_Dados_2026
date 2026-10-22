import io
import queue
import threading
import tkinter as tk
from tkinter import ttk

import requests
from PIL import Image, ImageTk

API_URL = "http://127.0.0.1:5000"
SPRITE_URL = (
    "https://raw.githubusercontent.com/PokeAPI/sprites/master/"
    "sprites/pokemon/other/official-artwork/{id}.png"
)
IMG_SIZE = (256, 256)

local_api = requests.Session()
local_api.trust_env = False


def describe_error(e):
    """Traduz a exceção em uma mensagem curta e útil."""
    if isinstance(e, requests.ConnectionError):
        return f"Não conectou em {API_URL}. A API (pokemon.py) está rodando?"
    if isinstance(e, requests.Timeout):
        return "A API demorou demais para responder."
    return f"{type(e).__name__}: {e}"


class PokedexApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pokédex")
        self.root.geometry("640x440")
        self.root.resizable(False, False)

        self.pokemons = []        # lista carregada da API
        self.image_cache = {}     # id -> PIL.Image
        self.photo = None         # referência obrigatória p/ o Tk não descartar a imagem
        self.results = queue.Queue()

        self._build_ui()
        self._poll_results()
        self.load_list()

    # ---------- Interface ----------
    def _build_ui(self):
        # Coluna esquerda: busca + lista
        left = ttk.Frame(self.root, padding=10)
        left.pack(side="left", fill="y")

        search_frame = ttk.Frame(left)
        search_frame.pack(fill="x", pady=(0, 8))
        self.search_var = tk.StringVar()
        entry = ttk.Entry(search_frame, textvariable=self.search_var, width=16)
        entry.pack(side="left", padx=(0, 4))
        entry.bind("<Return>", lambda e: self.search())
        ttk.Button(search_frame, text="Buscar", command=self.search).pack(side="left")

        list_frame = ttk.Frame(left)
        list_frame.pack(fill="both", expand=True)
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")
        self.listbox = tk.Listbox(
            list_frame, width=24, height=16, yscrollcommand=scrollbar.set, exportselection=False
        )
        self.listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.listbox.yview)
        self.listbox.bind("<<ListboxSelect>>", self.on_select)

        ttk.Button(left, text="Recarregar lista", command=self.load_list).pack(fill="x", pady=(8, 0))

        # Coluna direita: imagem + nome
        right = ttk.Frame(self.root, padding=10)
        right.pack(side="right", fill="both", expand=True)

        self.image_label = ttk.Label(right, text="Selecione um pokémon", anchor="center")
        self.image_label.pack(expand=True)

        self.name_label = ttk.Label(right, text="", font=("Helvetica", 16, "bold"))
        self.name_label.pack(pady=(8, 0))

        self.status_label = ttk.Label(right, text="", foreground="gray", wraplength=330, justify="center")
        self.status_label.pack(pady=(4, 0))

    def set_status(self, text, error=False):
        self.status_label.config(text=text, foreground="red" if error else "gray")

    # ---------- Threads (evita travar a janela) ----------
    def run_async(self, work, callback):
        def target():
            try:
                self.results.put((callback, work(), None))
            except Exception as e:
                self.results.put((callback, None, e))

        threading.Thread(target=target, daemon=True).start()

    def _poll_results(self):
        try:
            while True:
                callback, result, error = self.results.get_nowait()
                callback(result, error)
        except queue.Empty:
            pass
        self.root.after(100, self._poll_results)

    # ---------- Lista ----------
    def load_list(self):
        self.set_status("Carregando lista...")
        self.run_async(self._fetch_list, self._on_list_loaded)

    def _fetch_list(self):
        r = local_api.get(f"{API_URL}/pokemon", params={"limit": 200}, timeout=30)
        r.raise_for_status()
        return r.json()

    def _on_list_loaded(self, data, error):
        if error:
            self.set_status(describe_error(error), error=True)
            return
        self.pokemons = data
        self.listbox.delete(0, "end")
        for p in self.pokemons:
            self.listbox.insert("end", f"#{p['id']:03d}  {p['nome'].capitalize()}")
        if self.pokemons:
            self.set_status(f"{len(self.pokemons)} pokémons carregados")
        else:
            self.set_status(
                "A API respondeu, mas a lista está vazia. "
                "Veja no terminal do Flask se a PokeAPI foi acessada.",
                error=True,
            )

    # ---------- Seleção / busca ----------
    def on_select(self, event):
        selection = self.listbox.curselection()
        if selection:
            self.show_pokemon(self.pokemons[selection[0]])

    def search(self):
        term = self.search_var.get().strip().lower()
        if not term:
            return
        self.set_status("Buscando...")

        def work():
            r = local_api.get(f"{API_URL}/pokemon/{term}", timeout=30)
            if r.status_code == 404:
                return None
            r.raise_for_status()
            return r.json()

        def done(pokemon, error):
            if error:
                self.set_status(describe_error(error), error=True)
            elif pokemon is None:
                self.set_status("Pokémon não encontrado", error=True)
            else:
                self.show_pokemon(pokemon)

        self.run_async(work, done)

    # ---------- Exibição ----------
    def show_pokemon(self, pokemon):
        poke_id = pokemon["id"]
        self.name_label.config(text=f"#{poke_id:03d}  {pokemon['nome'].capitalize()}")

        if poke_id in self.image_cache:
            self._display_image(self.image_cache[poke_id])
            return

        self.set_status("Baixando imagem...")

        def work():
            r = requests.get(SPRITE_URL.format(id=poke_id), timeout=10)
            r.raise_for_status()
            img = Image.open(io.BytesIO(r.content)).convert("RGBA")
            img.thumbnail(IMG_SIZE)
            return img

        def done(img, error):
            if error:
                # Pokémons criados via POST (ids novos) não têm imagem na PokeAPI
                self.image_label.config(image="", text="Sem imagem disponível")
                self.photo = None
                self.set_status("Imagem não encontrada", error=True)
                return
            self.image_cache[poke_id] = img
            self._display_image(img)

        self.run_async(work, done)

    def _display_image(self, img):
        self.photo = ImageTk.PhotoImage(img)
        self.image_label.config(image=self.photo, text="")
        self.set_status("")


if __name__ == "__main__":
    root = tk.Tk()
    PokedexApp(root)
    root.mainloop()