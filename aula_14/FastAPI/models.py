from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils.types import ChoiceType

# cria a conexão do banco
db = create_engine("sqlite:///database.db")

# cria a base do banco de dados
base = declarative_base()

# cria as classes/tableas do banco
class User(base):
    # restrições da tabela
    __tablename__ = "users"
    
    id = Column("id", Integer, primary_key=True, autoincrement=True) 
    name = Column("name", String)
    email = Column("email", String, nullable=False) # não pode ser nulo
    password = Column("password", String)
    active = Column("active", Boolean)
    admin = Column("admin", Boolean, default=False) # por padrão não é admin

    # criação do usuário
    def __int__(self, name, email, password, active=True, admin=False):
        self.name = name
        self.email = email
        self.password = password
        self.active = active
        self.admin = admin

#
class Order(base):
    __tablename__ = "orders"

    # (("chave", valor))
    STATUS_ORDER = (
        ("PENDENTE", "PENDENTE"),
        ("CANCELADO", "CANCELADO"),
        ("FINALIZADO", "FINALIZADO")
    )

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    status = Column("status", ChoiceType(choices=STATUS_ORDER))
    user = Column("user", ForeignKey("users.id"))
    price = Column("price", Float)
    #itens =

    def __init__(self, user, status='PENDENTE', price=0):
        self.user = user
        self.price = price
        self.status = status

class ItemOrder(Base):
    __tablename__ = "item_orders"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    quantity = Column("quantity", Integer)
    price = Column("price", Float)
    order = Column("order", ForeignKey("orders.id"))

# executa a criação dos metadados do seu banco (cria efetivamente o banco de dados)