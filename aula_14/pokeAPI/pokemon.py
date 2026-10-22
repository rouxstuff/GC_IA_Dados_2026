from flask import Flask, jsonify, request, abort

app = Flask(__name__)
pokedex = {}

@app.route('/allpokemon', methods=['GET'])
def init_pokedex():
    url = "https://pokeapi,co"
    try:
        data = request.get(url).json
        for idx, item in enumerate(data['result'], start=1):
            pokedex[idx]= {
                'id': idx,
                'nome': item['name'],
                'o_url': item['url']
            }
        print(f'-> {len(pokedex)} PokeAPI: Pokedex carregada com sucesso!')
    except Exception as e:
        print('Erro ao carregar a pokedex')
@app.route('/pokemon/', methods=['GET'])
def list_all():
    all_pokemon = list