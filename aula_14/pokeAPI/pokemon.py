from flask import Flask, jsonify, request
import requests

app = Flask(__name__)
app.json.ensure_ascii = False

pokedex = {}

POKEAPI_URL = "https://pokeapi.co/api/v2/pokemon?limit=151"


def init_pokedex():
    """Carrega os pokémons da PokeAPI para a memória."""
    try:
        response = requests.get(POKEAPI_URL, timeout=10)
        response.raise_for_status()
        data = response.json()

        for item in data.get('results', []):
            # O ID real está no final da URL: .../pokemon/25/
            poke_id = int(item['url'].rstrip('/').split('/')[-1])
            pokedex[poke_id] = {
                'id': poke_id,
                'nome': item['name'],
                'o_url': item['url']
            }
        print(f'-> PokeAPI: {len(pokedex)} pokémons carregados com sucesso!')
    except requests.RequestException as e:
        print('Erro ao carregar a pokedex:', e)


# 1. GET - Listar pokémons (com paginação)
@app.route('/pokemon', methods=['GET'])
def list_all():
    page = max(request.args.get('page', 1, type=int), 1)
    limit = max(request.args.get('limit', 50, type=int), 1)
    start = (page - 1) * limit

    items = list(pokedex.values())[start:start + limit]
    return jsonify(items), 200


# 2. GET - Buscar um pokémon por ID ou nome
@app.route('/pokemon/<string:identificator>', methods=['GET'])
def search_pokemon(identificator):
    if identificator.isdigit():
        pokemon = pokedex.get(int(identificator))
        if pokemon:
            return jsonify(pokemon), 200

    name = identificator.lower()
    for pokemon in pokedex.values():
        if pokemon.get('nome') == name:
            return jsonify(pokemon), 200

    return jsonify({'erro': f"Pokémon '{identificator}' não encontrado na base local"}), 404


# 3. POST - Adicionar um novo pokémon
@app.route('/pokemon', methods=['POST'])
def add_pokemon():
    data = request.get_json(silent=True)
    if not data or not isinstance(data.get('nome'), str) or not data['nome'].strip():
        return jsonify({'erro': 'O campo nome é obrigatório e deve ser um texto'}), 400

    new_id = max(pokedex.keys(), default=0) + 1
    new_pokemon = {
        'id': new_id,
        'nome': data['nome'].strip().lower(),
        'tipo': data.get('tipo', 'desconhecido')
    }
    pokedex[new_id] = new_pokemon
    return jsonify(new_pokemon), 201


# 4. PUT - Atualizar um pokémon existente
@app.route('/pokemon/<int:poke_id>', methods=['PUT'])
def att_pokemon(poke_id):
    if poke_id not in pokedex:
        return jsonify({'erro': 'Pokémon não encontrado'}), 404

    data = request.get_json(silent=True)
    if not data:
        return jsonify({'erro': 'Corpo JSON inválido'}), 400

    if 'nome' in data:
        if not isinstance(data['nome'], str) or not data['nome'].strip():
            return jsonify({'erro': 'O campo nome deve ser um texto'}), 400
        pokedex[poke_id]['nome'] = data['nome'].strip().lower()

    if 'tipo' in data:
        pokedex[poke_id]['tipo'] = data['tipo']

    return jsonify(pokedex[poke_id]), 200


# 5. DELETE - Remover um pokémon
@app.route('/pokemon/<int:poke_id>', methods=['DELETE'])
def delete_pokemon(poke_id):
    if poke_id in pokedex:
        del pokedex[poke_id]
        return jsonify({'mensagem': f'Pokémon {poke_id} removido com sucesso'}), 200
    return jsonify({'erro': 'Pokémon não encontrado'}), 404


if __name__ == '__main__':
    init_pokedex()
    app.run(debug=True, use_reloader=False, port=5000)