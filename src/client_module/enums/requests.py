from enum import Enum

class Requests(Enum):
    CLOSECONNECTION = '0'    
    CADASTRO = '1'
    LOGIN = '2'
    SAQUE = '3'
    DEPOSITO  = '4'
    TRANSFERENCIA = '5'
    OBTERLISTACLIENTES = '6'
    CONSULTASALDO = '7'