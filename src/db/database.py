import sqlite3 as sql
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from models.cliente import Cliente

def criar_db():    
    con = sql.connect('clientes.db')
    cur = con.cursor()
    
    cur.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='clientes' ''')

    if cur.fetchone()[0] != 1 :
        cur.execute('''CREATE TABLE clientes
        (nome text, rg varchar(13), pin varchar(6), saldo real)''')
    
    if not __check_cliente_nome('admin'):
        cur.execute("INSERT INTO clientes VALUES ('admin', '12.345.678-90', '123456', 0)")

    con.commit()
    con.close()

def criar_cliente(cliente):
    con = sql.connect('clientes.db')
    cur = con.cursor()
    
    info_cliente = (cliente.get_nome(), cliente.get_rg(), cliente.get_pin(), cliente.get_saldo())

    if not __check_cliente_nome(cliente.get_nome()):
        cur.execute(''' INSERT INTO clientes VALUES (?,?,?,?) ''', info_cliente)
        print("Cliente com as informacoes: {}, {}, {}, {} foi inserido no banco de dados".format(info_cliente[0], info_cliente[1], info_cliente[2], info_cliente[3]))

    con.commit()
    con.close()
    

def autenticar_cliente(rg, pin):
    con = sql.connect('clientes.db')
    cur = con.cursor()
    authentication_failed = True

    if __check_cliente_rg(rg):
        cur.execute(''' SELECT count(*) FROM clientes WHERE rg=? AND pin=? ''', (rg, pin))
    
    query_result = cur.fetchall()
    print(query_result)

    if query_result is not None:
        authentication_failed = False

    con.close()
    return authentication_failed

# Checa se o cliente cujo nome é passado como parâmetro já existe no banco de dados.
def __check_cliente_nome(nome):
    con = sql.connect('clientes.db')
    cur = con.cursor()
    exists = True
  
    cur.execute(''' SELECT count(*) FROM clientes WHERE nome=? ''', (nome,))

    query_result = cur.fetchone()[0]

    if query_result == 0:
        exists = False
    
    con.close()
    return exists

def __check_cliente_rg(rg):
    con = sql.connect('clientes.db')
    cur = con.cursor()
    exists = True
  
    cur.execute(''' SELECT count(*) FROM clientes WHERE rg=? ''', (rg,))

    query_result = cur.fetchone()[0]

    if query_result == 0:
        exists = False
    
    con.close()
    return exists

def get_nome_cliente(rg):
    con = sql.connect('clientes.db')
    cur = con.cursor()

    cur.execute(''' SELECT nome, saldo FROM clientes WHERE rg=? ''', (rg,))

    data = cur.fetchall()[0]

    con.close()

    return data

def get_nomes_rg_clientes():
    con = sql.connect('clientes.db')
    cur = con.cursor()

    cur.execute(''' SELECT nome, rg FROM clientes ''')
    clientes = []
    clientes.concat(cur.fetchall())
    
    con.close()
    
    return (clientes)

def atualizar_saldo(valor, rg):
    con = sql.connect('clientes.db')
    cur = con.cursor()

    cur.execute(''' SELECT saldo FROM clientes WHERE rg=? ''', (rg))

    resultado = cur.fetchall()[0]
    
    con.close()

    return resultado