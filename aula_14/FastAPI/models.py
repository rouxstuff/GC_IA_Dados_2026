from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils.types import ChoiceType

# cria a conexão do banco
db = create_engine("sqlite:///database.db")

# cria a base do banco de dados
Base = declarative_base()

# cria as classes/tableas do banco
class User(Base):
    # restrições da tabela
    __tablename__ = "users"
    
    id = Column("id", Integer, primary_key=True, autoincrement=True) 
    name = Column("name", String)
    email = Column("email", String, nullable=False) # não pode ser nulo
    password = Column("password", String)
    active = Column("active", Boolean)
    admin = Column("admin", Boolean, default=False) # por padrão não é admin

    # criação do usuário
    def __init__(self, name, email, password, active=True, admin=False):
        self.name = name
        self.email = email
        self.password = password
        self.active = active
        self.admin = admin

#
class Order(Base):
    __tablename__ = "orders"

    # (("chave", valor))
    #STATUS_ORDER = (
       # ("PENDENTE", "PENDENTE"),
        #("CANCELADO", "CANCELADO"),
        #("FINALIZADO", "FINALIZADO")
    #)

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    status = Column("status", String)
    user = Column("user", ForeignKey("users.id"))
    price = Column("price", Float)
    #itens =

    def __init__(self, user, status='PENDENTE', price=0):
        self.user = user
        self.price = price
        self.status = status
#
class ItemOrder(Base):
    __tablename__ = "item_orders"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    quantity = Column("quantity", Integer)
    price = Column("price", Float)
    order = Column("order", ForeignKey("orders.id"))

    def __init__(self, quantity, price, order):
        self.quantity = quantity
        self.price = price
        self.order = order

#
# executa a criação dos metadados do seu banco (cria efetivamente o banco de dados)
