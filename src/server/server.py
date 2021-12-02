import socket
import os, sys
from _thread import *
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from db.database import *

server_socket = socket.socket()
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

def gerenciar_cliente_thread(conexao):
    conexao.send(str.encode('Bem vindo ao servidor'))

    while True:
        data = conexao.recv(2048)
        resposta = 'Resposta do servidor: ' + data.decode('utf-8')

        if not data:
            break
        conexao.sendall(str.encode(resposta))

    conexao.close()

while True:
    Client, endereco = server_socket.accept()
    print('Conectado a: ' + endereco[0] + ': ' + str(endereco[1]))
    start_new_thread(gerenciar_cliente_thread, (Client, ))
    cont_thread += 1
    print('Numero de threads: ' + str(cont_thread))

server_socket.close()