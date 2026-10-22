# 🧃- Casa de Sucos API

API desenvolvida com **Python** e **FastAPI**.
Integra com a API pública [Fruityvice](https://www.fruityvice.com/) para consultar as informações nutricionais das frutas e calcular as calorias e o açúcar de cada suco.

## Funcionalidade
- Consultar uma fruta na Fruityvice.
- Cadastrar sucos com nome, lista de frutas e descrição do gosto.
- Calcular automaticamente o total de calorias e de açúcar do suco (considerando **100 g de cada fruta**).
- Listar todos os sucos cadastrados com seus valores nutricionais.
- Atualizar as frutas de um suco e recalcular seus valores.
- Tratamento de erros com mensagens amigáveis (ex.: fruta não encontrada retorna HTTP 404).

## Tecnologias
- Python
- FastAPI
- Uvicorn
- Requests

## Estrutura do projeto
```
.
├── casa_de_sucos.py       # código-fonte da API
├── requirements.txt       # dependências
├── README.md              # este arquivo
└── evidencias_testes.md   # roteiro e evidências dos testes no Swagger
```
