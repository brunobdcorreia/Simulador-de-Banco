import socket
import pickle

client_socket = socket.socket()
host = '127.0.0.1'
porta = 1233

print('Aguardando conexao')

try:
    client_socket.connect((host, porta))
except socket.error as error:
    print(str(error))

resposta = client_socket.recv(1024)

while True:
    Input = input('Digite algo: ')
    client_socket.send(str.encode(Input))
    resposta = client_socket.recv(1024)
    print(resposta.decode('utf-8'))

client_socket.close()