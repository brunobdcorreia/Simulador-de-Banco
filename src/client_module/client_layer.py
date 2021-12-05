import socket
import sys, os
from enums.requests import Requests

host = '127.0.0.1'
porta = 1233

BUFFER_SIZE = 1024

def enviar_request_cadastro(nome, rg, pin):  
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:  
        try:
            client_socket.connect((host, porta))

            if client_socket.recv(BUFFER_SIZE).decode('utf-8') == 'Bem vindo ao servidor':
                request_cadastro = Requests.CADASTRO.value + '#' + nome + '#' + rg + '#' + pin
                client_socket.send(str.encode(request_cadastro))

                if client_socket.recv(BUFFER_SIZE).decode('utf-8') == 'ok': 
                    client_socket.close()                     
                    return True
                else:
                    client_socket.close()
                    return False
            else:
                client_socket.close()
                return False

        except socket.error as error:
            print(str(error))
            return False

def enviar_request_login(rg, pin):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:  
        try:
            client_socket.connect((host, porta))
            if client_socket.recv(BUFFER_SIZE).decode('utf-8') == 'Bem vindo ao servidor':
                request_cadastro = Requests.LOGIN.value + '#' + rg + '#' + pin
                client_socket.send(str.encode(request_cadastro))
                resposta = client_socket.recv(BUFFER_SIZE).decode('utf-8')
                print('Resposta:')
                print(resposta.split('#'))
                
                return (True, str(resposta).split('#'))
            else:
                return (False,)

        except socket.error as error:
            print(str(error))
            return (False,)
            
def enviar_request_saque(valor, rg):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:  
        try:
            client_socket.connect((host, porta))
            if client_socket.recv(BUFFER_SIZE).decode('utf-8') == 'Bem vindo ao servidor':
                request_saque = Requests.SAQUE.value + '#' + valor + '#' + rg
                client_socket.send(str.encode(request_saque))
                resposta = client_socket.recv(BUFFER_SIZE).decode('utf-8')

                if resposta == 'ACCEPT':
                    return True
            else: return False

        except socket.error as error:
            print(str(error))
           

def obter_lista_clientes():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:  
        try:
            client_socket.connect((host, porta))
            if client_socket.recv(BUFFER_SIZE).decode('utf-8') == 'Bem vindo ao servidor':
                print('Requisitou no client layer')
                
                request = Requests.OBTERLISTACLIENTES.value
                client_socket.send(str.encode(request))
                
                print('Fez a requisição ao servidor. Aguardando resposta.')
                
                resposta = client_socket.recv(BUFFER_SIZE).decode('utf-8')
                # TODO : Tratar resposta do backend
                return (True,)
                
        except socket.error as error:
            print(str(error))