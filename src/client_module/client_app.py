import sys, os

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from client_layer import *
from gui.gui import *


if __name__ == '__main__':
    criar_janela_inicio()