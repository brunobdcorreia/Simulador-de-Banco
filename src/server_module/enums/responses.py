from enum import Enum

class Responses(Enum):
    INTERNAL_ERROR = '0'
    CONNECTED = '1'
    SUCCESS = '2'
    FORBIDDEN = '3'