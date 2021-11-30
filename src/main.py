from gui import gui as ui
from db import database as db
from models.cliente import Cliente

db.criar_db()

c = Cliente('Braia', '23.476.987-32', 1234.56)

db.criar_cliente(c)