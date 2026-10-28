```
para rodar o código digite: uvicorn main:app --reload

- ele cria um servidor utilizando uvicorn e executa o arquivo main.py
        - app é a variavel do FastAPI

Rest APIs
GET -> leitura/pegar
POST -> enviar/criar
PUT/PATCH -> edição
DELET -> deletar
```


## 📦 Dependências

| Pacote | Para que serve |
|--------|----------------|
| **fastapi** | Framework web moderno e rápido para criar APIs em Python. Fornece roteamento, validação de dados (via Pydantic), injeção de dependências e documentação automática (Swagger em `/docs` e ReDoc em `/redoc`). |
| **uvicorn** | Servidor ASGI que executa a aplicação FastAPI. É ele que "sobe" a API e recebe as requisições HTTP. |
| **sqlalchemy** | ORM e toolkit de banco de dados. Permite definir tabelas como classes Python e fazer consultas sem escrever SQL manualmente. |
| **passlib[bcrypt]** | Biblioteca de hash de senhas. O extra `[bcrypt]` instala o algoritmo bcrypt, usado para armazenar senhas de forma segura (nunca em texto puro) e verificá-las no login. |
| **python-jose[cryptography]** | Criação e validação de tokens JWT (JSON Web Tokens), usados na autenticação. O extra `[cryptography]` fornece o backend criptográfico para assinar os tokens. |
| **python-dotenv** | Carrega variáveis de ambiente de um arquivo `.env` (ex.: `SECRET_KEY`, `DATABASE_URL`), mantendo credenciais fora do código. |
| **python-multipart** | Permite o parsing de dados `multipart/form-data` e `x-www-form-urlencoded`. É necessário no FastAPI para receber formulários e uploads de arquivos, e também para o `OAuth2PasswordRequestForm` usado no login. |

### Instalação

```bash
pip install -r requirements.txt
```