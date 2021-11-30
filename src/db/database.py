import sqlite3 as sql
from models.cliente import Cliente
import sys
import os

def criar_db():    
    con = sql.connect('clientes.db')
    cur = con.cursor()
    
    cur.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='clientes' ''')

    if cur.fetchone()[0] != 1 :
        cur.execute('''CREATE TABLE clientes
        (nome text, rg varchar(13), saldo real)''')
    
    if not __check_cliente('admin'):
        cur.execute("INSERT INTO clientes VALUES ('admin', '12.345.678-90', 23499.99)")

    con.commit()
    con.close()

def criar_cliente(cliente):
    con = sql.connect('clientes.db')
    cur = con.cursor()
    
    info_cliente = (cliente.get_nome(), cliente.get_rg(), cliente.get_saldo())

    if not __check_cliente(cliente.get_nome()):
        cur.execute(''' INSERT INTO clientes VALUES (?,?,?) ''', info_cliente)
        print("Cliente com as informacoes: {}, {}, {} foi inserido no banco de dados".format(info_cliente[0], info_cliente[1], info_cliente[2]))

    con.commit()
    con.close()

# Checa se o cliente cujo nome é passado como parâmetro já existe no banco de dados.
def __check_cliente(nome):
    con = sql.connect('clientes.db')
    cur = con.cursor()
    exists = True
  
    cur.execute(''' SELECT count(*) FROM clientes WHERE nome=? ''', (nome,))

    query_result = cur.fetchone()[0]

    if query_result == 0:
        exists = False
    
    con.close()
    return exists