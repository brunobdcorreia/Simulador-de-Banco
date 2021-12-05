import socket
import sys, os
from enums.requests import Requests
from enums.responses import Responses

host = '127.0.0.1'
porta = 1233

BUFFER_SIZE = 1024
MENSAGEM_ERRO_DESCONHECIDO = 'Erro desconhecido'
MENSAGEM_SERVIDOR_SEM_RESPOSTA = 'Erro de conexão com o servidor: sem resposta'


def enviar_request_cadastro(nome, rg, pin):  
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((host, porta))

            if Responses(client_socket.recv(BUFFER_SIZE).decode('utf-8')) == Responses.CONNECTED:
                request_cadastro = Requests.CADASTRO.value + '#' + nome + '#' + rg + '#' + pin
                client_socket.send(str.encode(request_cadastro))
                
                resposta = client_socket.recv(BUFFER_SIZE).decode('utf-8')
                status = Responses(resposta)
                if status == Responses.SUCCESS: 
                    return (Responses.SUCCESS,)
                else:
                    return (Responses.INTERNAL_ERROR, MENSAGEM_ERRO_DESCONHECIDO)
            else:
                return (Responses.INTERNAL_ERROR, MENSAGEM_ERRO_DESCONHECIDO)
        except socket.error as error:
            print(str(error))
            return (Responses.INTERNAL_ERROR, str(error))

def enviar_request_login(rg, pin):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((host, porta))        
            if Responses(client_socket.recv(BUFFER_SIZE).decode('utf-8')) == Responses.CONNECTED:
                request_cadastro = Requests.LOGIN.value + '#' + rg + '#' + pin
                client_socket.send(str.encode(request_cadastro))
                
                resposta = client_socket.recv(BUFFER_SIZE).decode('utf-8')
                resposta = resposta.split('#')
                status = Responses(resposta[0])

                if status == Responses.SUCCESS:
                    nome = resposta[1]
                    saldo = resposta[2]

                    return (Responses.SUCCESS, nome, saldo)
                else:
                    return (Responses.INTERNAL_ERROR, MENSAGEM_ERRO_DESCONHECIDO)
            else:
                return (Responses.INTERNAL_ERROR, MENSAGEM_SERVIDOR_SEM_RESPOSTA)

        except socket.error as error:
            print(str(error))
            return (Responses.INTERNAL_ERROR, str(error))
            
def enviar_request_saque(valor, rg):  
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:    
            client_socket.connect((host, porta))
            if Responses(client_socket.recv(BUFFER_SIZE).decode('utf-8')) == Responses.CONNECTED:        
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
            return (Responses.INTERNAL_ERROR, str(error))

def enviar_request_deposito(valor, rg):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            print(client_socket)
            client_socket.connect((host, porta))
            if Responses(client_socket.recv(BUFFER_SIZE).decode('utf-8')) == Responses.CONNECTED:        
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
            return (Responses.INTERNAL_ERROR, str(error))

def enviar_request_transferencia(valor, rg, rg_favorecido):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((host, porta))
            if Responses(client_socket.recv(BUFFER_SIZE).decode('utf-8')) == Responses.CONNECTED:  
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
            return (Responses.INTERNAL_ERROR, str(error))

def consultar_saldo_request(rg):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((host, porta))
            if Responses(client_socket.recv(BUFFER_SIZE).decode('utf-8')) == Responses.CONNECTED:
                request_consulta = Requests.CONSULTA_SALDO.value + '#' + rg
                client_socket.send(str.encode(request_consulta))
                
                resposta = client_socket.recv(BUFFER_SIZE).decode('utf-8')
                resposta = resposta.split('#')

                status = resposta[0] 
                if status == Responses.SUCCESS.value:
                    saldo = resposta[1]
                    return (Responses.SUCCESS, saldo)
                else:
                    mensagem = resposta[1]
                    return (status, mensagem)
            else: 
                return (Responses.INTERNAL_ERROR, MENSAGEM_SERVIDOR_SEM_RESPOSTA)
                
        except socket.error as error:
                print(str(error))
                return (Responses.INTERNAL_ERROR, str(error))

def obter_lista_clientes():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:  
            client_socket.connect((host, porta))
            if Responses(client_socket.recv(BUFFER_SIZE).decode('utf-8')) == Responses.CONNECTED:             
                request = Requests.OBTER_LISTA_CLIENTES.value
                client_socket.send(str.encode(request))
                
                resposta = client_socket.recv(BUFFER_SIZE).decode('utf-8')
                resposta = resposta.split('#')
                status = Responses(resposta[0])

                if status == Responses.SUCCESS:                        
                    # Removendo caracteres extras 
                    conteudo = resposta[1]
                    conteudo = conteudo.replace('[', '')
                    conteudo = conteudo.replace(')]', '')
                    conteudo = conteudo.replace('(', '')
                    conteudo = conteudo.replace('\'', '')

                    # Estruturando retorno para o GUI
                    conteudo = conteudo.split('), ')

                    listaClientes = []
                    for resposta_cliente in conteudo:
                        resposta_cliente = resposta_cliente.replace(',', ' -')
                        listaClientes.append(resposta_cliente)

                    return (Responses.SUCCESS, listaClientes)
                else:
                    return (Responses.INTERNAL_ERROR, MENSAGEM_ERRO_DESCONHECIDO)
            else: 
                return (Responses.INTERNAL_ERROR, MENSAGEM_SERVIDOR_SEM_RESPOSTA)
                    
        except socket.error as error:
            print(str(error))
            return (Responses.INTERNAL_ERROR, str(error))
