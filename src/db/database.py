import sqlite3 as sql
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from models.cliente import Cliente

def criar_db():    
    '''
    Cria a instância do banco de dados
    '''
    with sql.connect('clientes.db') as con:
        cur = con.cursor()
        
        cur.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='clientes' ''')

        if cur.fetchone()[0] != 1 :
            cur.execute('''CREATE TABLE clientes
            (nome text, rg varchar(13), pin varchar(6), saldo real)''')
        
        if not __check_cliente_nome('admin'):
            cur.execute("INSERT INTO clientes VALUES ('admin', '12.345.678-90', '123456', 0)")

        con.commit()

def criar_cliente(cliente):
    '''
    Cadastra um novo cliente
    '''
    with sql.connect('clientes.db') as con:
        cur = con.cursor()
        
        info_cliente = (cliente.get_nome(), cliente.get_rg(), cliente.get_pin(), cliente.get_saldo())

        if not __check_cliente_nome(cliente.get_nome()):
            cur.execute(''' INSERT INTO clientes VALUES (?,?,?,?) ''', info_cliente)

        con.commit()        

def autenticar_cliente(rg, pin):
    '''
    Verifica se o usuário exsite e os dados estão corretos
    '''
    with sql.connect('clientes.db') as con:
        cur = con.cursor()
        authentication_failed = True

        if __check_cliente_rg(rg):
            cur.execute(''' SELECT count(*) FROM clientes WHERE rg=? AND pin=? ''', (rg, pin))
        
        query_result = cur.fetchall()

        if query_result is not None:
            authentication_failed = False

        return authentication_failed

def __check_cliente_nome(nome):
    '''
    Checa se o cliente cujo nome é passado como parâmetro já existe no banco de dados.
    '''
    with sql.connect('clientes.db') as con:
        cur = con.cursor()
        exists = True
    
        cur.execute(''' SELECT count(*) FROM clientes WHERE nome=? ''', (nome,))

        query_result = cur.fetchone()[0]

        if query_result == 0:
            exists = False
        
        return exists

def __check_cliente_rg(rg):
    '''
    Verifica se o cliente existe a partir do rg fornecido
    '''
    with sql.connect('clientes.db') as con:
        cur = con.cursor()
        exists = True
    
        cur.execute(''' SELECT count(*) FROM clientes WHERE rg=? ''', (rg,))

        query_result = cur.fetchone()[0]

        if query_result == 0:
            exists = False
        
        return exists

def get_nome_cliente(rg):
    '''
    Obtém o nome e o saldo cliente a partir do rg cadastrado
    '''
    with sql.connect('clientes.db') as con:
        cur = con.cursor()

        cur.execute(''' SELECT nome, saldo FROM clientes WHERE rg=? ''', (rg,))

        nome, saldo = cur.fetchall()[0]

        return (nome, saldo)

def get_rg_nomes_clientes():
    '''
    Obtem uma lista com o rg e o nome de todos os clientes cadastrados no banco
    '''
    with sql.connect('clientes.db') as con:
        cur = con.cursor()

        cur.execute(''' SELECT rg, nome FROM clientes where nome!='admin' ''')
        clientes = [] + cur.fetchall()        
        
        return (clientes)

def get_saldo(rg):
    '''
    Obtem o saldo de um cliente a partir do seu rg
    '''
    with sql.connect('clientes.db') as con:
        cur = con.cursor()

        cur.execute(''' SELECT saldo from clientes where rg=? ''', (rg,))
        saldo = cur.fetchall()[0]

        return saldo[0]

def atualizar_saldo(valor, rg):
    '''
    Atualiza o saldo de um cliente a partir do seu rg
    '''
    with sql.connect('clientes.db') as con:
        cur = con.cursor()

        cur.execute(''' UPDATE clientes SET saldo=? WHERE rg=? ''', (valor, rg,))
        
        con.commit()    
        