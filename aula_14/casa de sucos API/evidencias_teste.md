# Evidências dos testes no Swagger
 Testes feitos em `http://127.0.0.1:8000/docs` com a API rodando localmente.

## Teste 1: GET /frutas/banana
 
- **Requisição:** `GET /frutas/banana`
- **Resposta esperada (200):**
```json
  { "nome": "Banana", "calorias": 96, "acucar": 17.2 }
```

## Teste 2: GET /frutas/abacaxi (fruta inexistente)
 
- **Requisição:** `GET /frutas/abacaxi`
- **Resposta esperada (404):**
```json
  { "detail": "Fruta 'abacaxi' não encontrada. Use o nome em inglês (ex.: banana)." }
```

## Teste 3: POST /sucos
 
- **Corpo:**
```json
  {
    "nome": "Vitamina Tropical",
    "frutas": ["banana", "strawberry"],
    "tem_gosto_de": "Tamarindo"
  }
```
- **Resposta esperada (201):**
```json
  {
    "id": 1,
    "nome": "Vitamina Tropical",
    "frutas": ["banana", "strawberry"],
    "tem_gosto_de": "Tamarindo",
    "total_calorias": 125,
    "total_acucar": 22.6
  }
```

## Teste 4: POST /sucos com fruta inexistente
 
- **Corpo:**
```json
  {
    "nome": "Suco Invalido",
    "frutas": ["banana", "abacaxi"],
    "tem_gosto_de": "Teste"
  }
```
- **Resposta esperada (404):** mensagem informando que `abacaxi` não foi encontrada.
## Teste 5: POST /sucos sem frutas
 
- **Corpo:**
```json
  { "nome": "Suco Vazio", "frutas": [], "tem_gosto_de": "Nada" }
```
- **Resposta esperada (400):**
```json
  { "detail": "O campo 'frutas' deve ser uma lista com pelo menos uma fruta." }
```
## Teste 6: GET /sucos
 
- **Resposta esperada (200):** lista com apenas o suco do teste 3 (o do teste 4 não foi salvo).
## Teste 7: PUT /sucos/1
 
- **Corpo:**
```json
  { "frutas": ["mango", "banana"] }
```
- **Resposta esperada (200):** o mesmo suco, com `frutas` trocadas e `total_calorias` / `total_acucar` recalculados.
## Teste 8: PUT /sucos/99 (suco inexistente)
 
- **Corpo:**
```json
  { "frutas": ["banana"] }
```
- **Resposta esperada (404):**
```json
  { "detail": "Suco 99 não encontrado." }
```