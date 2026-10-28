from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

# cria a conexão do banco
db = create_engine("sqlite:///database.db")

# cria a base do banco de dados
base = declarative_base()
# cria as classes/tableas do banco
# executa a criação dos metadados do seu banco (cria efetivamente o banco de dados)