import socket
import sys, os

host = '127.0.0.1'
porta = 1233

def enviar_request_cadastro(nome, rg, pin):  
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:  
        try:
            client_socket.connect((host, porta))

            if client_socket.recv(1024).decode('utf-8') == 'Bem vindo ao servidor':
                request_cadastro = 'cadastro.' + nome + '.' + rg + '.' + pin
                client_socket.sendall(str.encode(request_cadastro))

                if client_socket.recv(1024).decode('utf-8') == 'ok': 
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

def enviar_request_login(rg, pin):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:  
        try:
            client_socket.connect((host, porta))
            if client_socket.recv(1024).decode('utf-8') == 'Bem vindo ao servidor':
                request_cadastro = 'login.' + rg + '.' + pin
                client_socket.sendall(str.encode(request_cadastro))
                resposta = client_socket.recv(1024)
                print('Resposta:')
                print(resposta)
                return True
            else:
                return False

        except socket.error as error:
            print(str(error))