import requests
import uvicorn
from fastapi import FastAPI, HTTPException

app = FastAPI(title="Casa de Sucos API")

sucos = []  # lista em memória


def buscar_fruta(nome):
    """Consulta a Fruityvice e devolve nome, calorias e açúcar."""
    resp = requests.get(f"https://www.fruityvice.com/api/fruit/{nome.strip().lower()}", timeout=10)
    if resp.status_code != 200:
        raise HTTPException(404, f"Fruta '{nome}' não encontrada. Use o nome em inglês (ex.: banana).")

    dados = resp.json()
    return {
        "nome": dados["name"],
        "calorias": dados["nutritions"]["calories"],
        "acucar": dados["nutritions"]["sugar"],
    }


def somar(frutas):
    """Soma calorias e açúcar (100 g de cada fruta)."""
    if not isinstance(frutas, list) or len(frutas) == 0:
        raise HTTPException(400, "O campo 'frutas' deve ser uma lista com pelo menos uma fruta.")

    calorias = 0
    acucar = 0
    for nome in frutas:
        fruta = buscar_fruta(str(nome))
        calorias += fruta["calorias"]
        acucar += fruta["acucar"]
    return round(calorias, 2), round(acucar, 2)


# 1. Consultar uma fruta
@app.get("/frutas/{nome}")
def get_fruta(nome: str):
    return buscar_fruta(nome)


# 2. Cadastrar um suco  (o JSON chega como dicionário)
@app.post("/sucos", status_code=201)
def criar_suco(body: dict):
    for campo in ["nome", "frutas", "tem_gosto_de"]:
        if campo not in body:
            raise HTTPException(400, f"O campo '{campo}' é obrigatório.")

    calorias, acucar = somar(body["frutas"])
    suco = {
        "id": len(sucos) + 1,
        "nome": body["nome"],
        "frutas": body["frutas"],
        "tem_gosto_de": body["tem_gosto_de"],
        "total_calorias": calorias,
        "total_acucar": acucar,
    }
    sucos.append(suco)
    return suco


# 3. Listar os sucos
@app.get("/sucos")
def listar_sucos():
    return sucos


# Bônus: atualizar as frutas de um suco
@app.put("/sucos/{suco_id}")
def atualizar_suco(suco_id: int, body: dict):
    if "frutas" not in body:
        raise HTTPException(400, "O campo 'frutas' é obrigatório.")

    for suco in sucos:
        if suco["id"] == suco_id:
            calorias, acucar = somar(body["frutas"])
            suco["frutas"] = body["frutas"]
            suco["total_calorias"] = calorias
            suco["total_acucar"] = acucar
            return suco
    raise HTTPException(404, f"Suco {suco_id} não encontrado.")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)