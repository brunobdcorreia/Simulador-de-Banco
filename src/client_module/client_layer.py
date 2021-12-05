import socket
import sys, os
from enums.requests import Requests
from enums.responses import Responses

host = '127.0.0.1'
porta = 1233

BUFFER_SIZE = 1024
MENSAGEM_SERVIDOR_SEM_RESPOSTA = 'Erro de conexão com o servidor: sem resposta'

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
                return (False, MENSAGEM_SERVIDOR_SEM_RESPOSTA)

        except socket.error as error:
            print(str(error))
            return (False,)
            
def enviar_request_saque(valor, rg):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:  
        try:
            client_socket.connect((host, porta))
            if client_socket.recv(BUFFER_SIZE).decode('utf-8') == 'Bem vindo ao servidor':
                request_saque = Requests.SAQUE.value + '#' + str(valor) + '#' + rg
                client_socket.send(str.encode(request_saque))
                resposta = client_socket.recv(BUFFER_SIZE).decode('utf-8')
                
                resposta = resposta.split('#')
                status = Responses(resposta[0])

                if status == Responses.SUCCESS:
                    novo_saldo = resposta[1]
                    return (Responses.SUCCESS, novo_saldo)
                else:
                    mensagem = resposta[1]
                    return (status, mensagem)
            else: 
                return (Responses.INTERNAL_ERROR, MENSAGEM_SERVIDOR_SEM_RESPOSTA)

        except socket.error as error:
            print(str(error))

def enviar_request_deposito(valor, rg):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:  
        try:
            client_socket.connect((host, porta))
            if client_socket.recv(BUFFER_SIZE).decode('utf-8') == 'Bem vindo ao servidor':
                request_saque = Requests.DEPOSITO.value + '#' + valor + '#' + rg
                client_socket.send(str.encode(request_saque))
                
                resposta = client_socket.recv(BUFFER_SIZE).decode('utf-8')
                resposta = resposta.split('#')

                status = Responses(resposta[0])
                if status == Responses.SUCCESS:
                    novo_saldo = resposta[1]
                    return (Responses.SUCCESS, novo_saldo)
                else:
                    mensagem = resposta[1]
                    return (status, mensagem)
            else: 
                return (Responses.INTERNAL_ERROR, MENSAGEM_SERVIDOR_SEM_RESPOSTA)

        except socket.error as error:
            print(str(error))

def enviar_request_transferencia(valor, rg, rg_favorecido):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:  
        try:
            client_socket.connect((host, porta))
            if client_socket.recv(BUFFER_SIZE).decode('utf-8') == 'Bem vindo ao servidor':
                request_transf = Requests.TRANSFERENCIA.value + '#' + valor + '#' + rg + '#' + rg_favorecido
                client_socket.send(str.encode(request_transf))
                
                resposta = client_socket.recv(BUFFER_SIZE).decode('utf-8')
                resposta = resposta.split('#')

                status = resposta[0] 
                if status == Responses.SUCCESS.value:
                    novo_saldo = resposta[1]
                    novo_saldo_favorecido = resposta[2]
                    return (Responses.SUCCESS, novo_saldo, novo_saldo_favorecido)
                else:
                    # Retorno o erro e a mensagem
                    return resposta
            else: 
                return (Responses.INTERNAL_ERROR, MENSAGEM_SERVIDOR_SEM_RESPOSTA)

        except socket.error as error:
            print(str(error))

def obter_lista_clientes():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:  
        try:
            client_socket.connect((host, porta))
            if client_socket.recv(BUFFER_SIZE).decode('utf-8') == 'Bem vindo ao servidor':                
                request = Requests.OBTERLISTACLIENTES.value
                client_socket.send(str.encode(request))
                
                resposta = client_socket.recv(BUFFER_SIZE).decode('utf-8')
                
                # Removendo caracteres extras 
                resposta = resposta.replace('[', '')
                resposta = resposta.replace(')]', '')
                resposta = resposta.replace('(', '')
                resposta = resposta.replace('\'', '')

                # Estruturando retorno para o GUI
                resposta = resposta.split('), ')

                listaClientes = []
                for respostaCliente in resposta:
                    respostaCliente = respostaCliente.replace(',', ' -')
                    listaClientes.append(respostaCliente)

                return (True, listaClientes)
            else:
                return (False, MENSAGEM_SERVIDOR_SEM_RESPOSTA)
                
        except socket.error as error:
            print(str(error))