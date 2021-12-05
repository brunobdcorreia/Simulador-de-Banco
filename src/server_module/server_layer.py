import socket
import os, sys
from _thread import *
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from db.database import *
from models.cliente import *
from enums.requests import Requests
from enums.responses import Responses

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
porta = 1233
cont_thread = 0

criar_db()

try:
    server_socket.bind((host, porta))
except socket.error as error:
    print(str(error))

print('Aguardando conexão...')
server_socket.listen(5)

def gerenciar_cliente_thread(conexao, endereco):
    conexao.send(str.encode(Responses.CONNECTED.value))
    while True:
        data = conexao.recv(2048)
        req = data.decode('utf-8')
        req_header = str(req).split('#')

        if not data: 
            break

        handle_request(req_header, conexao, endereco)
    
    conexao.close()

def handle_request(req, conn, endereco):
    if Requests(req[0]) == Requests.CADASTRO:
        cliente = Cliente(
            nome=req[1], 
            rg=req[2], 
            pin=req[3])
        criar_cliente(cliente)
        conn.send(str.encode(Responses.SUCCESS.value))

    elif Requests(req[0]) == Requests.LOGIN:
        if not autenticar_cliente(req[1], req[2]):
            print('Login com sucesso')
            print(conn.getsockname())
            print(conn.getpeername())
            print('Mandando para', conn.getsockname())
            cliente_nome, cliente_saldo = get_nome_cliente(req[1])
            conn.send(str.encode(Responses.SUCCESS.value + '#' + cliente_nome + '#' + str(cliente_saldo)))
        else:
            print('Login falhou')
            conn.send(str.encode('falha'))

    elif Requests(req[0]) == Requests.SAQUE:
        valor = float(req[1])
        rg = req[2]
        
        saldo_atual = get_saldo(rg)

        # Verifica se há saldo
        if saldo_atual < valor:
            conn.send(str.encode(Responses.FORBIDDEN.value + '#' + 'Saldo insuficiente'))
        else:
            # Realiza o saque
            saldo_novo = saldo_atual - valor
            atualizar_saldo(saldo_novo, rg)
            conn.send(str.encode(Responses.SUCCESS.value + '#' + str(saldo_novo)))

    elif Requests(req[0]) == Requests.DEPOSITO:
        valor = float(req[1])
        rg = req[2]
        
        saldo_atual = get_saldo(rg)
        saldo_novo = saldo_atual + valor
        
        # Realiza o depósito
        atualizar_saldo(saldo_novo, rg)

        #TODO: Tirar debug
        print('Saldo pós depósito: ' + str(get_saldo(rg)))
        conn.send(str.encode(Responses.SUCCESS.value + '#' + str(saldo_novo)))

    elif Requests(req[0]) == Requests.TRANSFERENCIA:
        valor = float(req[1])
        rg = req[2]
        rg_favorecido = req[3]

        saldo_atual = get_saldo(rg)
        saldo_atual_favorecido = get_saldo(rg_favorecido)

        if saldo_atual < valor:
            conn.send(str.encode(Responses.FORBIDDEN.value + '#' + 'Saldo insuficiente'))
        else:
            saldo_novo = saldo_atual - valor
            atualizar_saldo(saldo_novo, rg)
            saldo_novo_favorecido = saldo_atual_favorecido + valor
            atualizar_saldo(saldo_novo_favorecido, rg_favorecido)
            conn.send(str.encode(Responses.SUCCESS.value + '#' + str(saldo_novo) + '#' + str(saldo_novo_favorecido)))

    elif Requests(req[0]) == Requests.OBTER_LISTA_CLIENTES:
        clientes = get_rg_nomes_clientes()
        conn.send(str.encode(Responses.SUCCESS.value + '#' + str(clientes)))

    elif Requests(req[0]) == Requests.CONSULTA_SALDO:
        saldo = get_saldo(req[1])
        print("Consulta saldo retornou: {}".format(saldo))
        conn.send(str.encode(Responses.SUCCESS.value + '#' + str(saldo)))
        

while True:
    client_socket, endereco = server_socket.accept()
    print('Conectado a: ' + endereco[0] + ': ' + str(endereco[1]))
    start_new_thread(gerenciar_cliente_thread, (client_socket, endereco))
    cont_thread += 1
    print('Numero de threads: ' + str(cont_thread))

server_socket.close()