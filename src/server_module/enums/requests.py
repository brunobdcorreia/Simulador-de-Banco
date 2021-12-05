from enum import Enum

class Requests(Enum):
    CLOSE_CONNECTION = '0'
    CADASTRO = '1'
    LOGIN = '2'
    SAQUE = '3'
    DEPOSITO  = '4'
    TRANSFERENCIA = '5'
    OBTER_LISTA_CLIENTES = '6'
    CONSULTA_SALDO = '7'