from tkinter import messagebox, StringVar
from models.cliente import Cliente
from db.database import criar_cliente, autenticar_cliente, get_nome_cliente
import tkinter as tk
import sys, os
from tkinter.messagebox import *

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from client_module.client_layer import *

def __criar_tela_principal(nome, rg, saldo):
    try:
        window = tk.Tk("Banco")
        window.title('Banco do Bruhsil')
        frm_main = tk.Frame(window)
        frm_sub = tk.Frame(master=frm_main, relief=tk.RIDGE, borderwidth=5)
        lbl_banco = tk.Label(master=frm_main, text="Banco do Bruhsil")

        # Criar submenu a esquerda com nome, rg e saldo
        frm_menu = tk.Frame(master=frm_sub, relief=tk.RIDGE, borderwidth=5)
        lbl_dados = tk.Label(master=frm_menu, text="Dados do cliente")
        lbl_nome = tk.Label(master=frm_menu, text="Nome: " + nome)
        lbl_rg = tk.Label(master=frm_menu, text= "rg: " + rg)
        lbl_saldo = tk.Label(master=frm_menu, text="Saldo: " + str(saldo))

        # Criar submenu a direita com botões para transferir e retirar
        btn_transferir = tk.Button(master=frm_sub, text="Realizar transferencia", command=__mostrar_janela_transferir)
        btn_retirar = tk.Button(master=frm_sub, text="Retirar", command=lambda: __mostrar_tela_retirar(rg))

        btn_transferir.pack(side=tk.RIGHT)
        btn_retirar.pack(side=tk.RIGHT)
        lbl_dados.pack()
        lbl_nome.pack()
        lbl_rg.pack()
        lbl_saldo.pack()
        frm_menu.pack(side=tk.LEFT, padx=5, pady=5)

        lbl_banco.pack()
        frm_sub.pack()
        frm_main.pack(side=tk.TOP)

        window.mainloop()
    except Exception as e:
        print(e)
        __mostrar_janela_erro(e)

def criar_janela_inicio():
    try:
        global tela_inicio
        tela_inicio = tk.Tk('Login')
        tela_inicio.geometry('300x250')
        tela_inicio.resizable(height=None, width=None)

        intro_lbl = tk.Label(text="Banco do Bruhsil", bg="blue", width="300", height="2", font=("Calibri", 13), fg='white').pack()
        tk.Label(text='').pack()
        login_btn = tk.Button(text='Login', height='2', width='30', command=__criar_janela_login)
        login_btn.pack()
        tk.Label(text='').pack()

        register_btn = tk.Button(text='Cadastrar', height='2', width='30', command=__criar_janela_cadastro)
        register_btn.pack()

        tela_inicio.mainloop()
    except Exception as e:
        print(e)
        __mostrar_janela_erro(e)

def __criar_janela_login():
    try:
        global tela_login
        tela_login = tk.Toplevel(tela_inicio)
        tela_login.title('Realizar login')
        tela_login.geometry('300x250')

        global rg_verificar
        global pin_verificar

        rg_verificar = tk.StringVar()
        pin_verificar = tk.StringVar()

        tk.Label(tela_login, text="Insira suas credenciais", bg="blue", fg='white').pack()
        tk.Label(tela_login, text="").pack()

        rg_lbl = tk.Label(tela_login, text='RG *')
        rg_lbl.pack()

        global rg_ent_login
        rg_ent_login = tk.Entry(tela_login, textvariable=rg_verificar)
        rg_ent_login.pack()

        pin_lbl = tk.Label(tela_login, text='PIN *')
        pin_lbl.pack()

        global pin_ent_login
        pin_ent_login = tk.Entry(tela_login, show='*', textvariable=pin_verificar)
        pin_ent_login.pack()

        tk.Label(tela_login, text="").pack()

        login_btn = tk.Button(tela_login, text='Login', height='2', width='30', command=__realizar_login)
        login_btn.pack()
    except Exception as e:
        print(e)
        __mostrar_janela_erro(e)


def __realizar_login():
    try:
        info_rg = rg_ent_login.get()
        info_pin = pin_ent_login.get()
        
        resposta_login = enviar_request_login(info_rg, info_pin)

        assert resposta_login[0], 'Erro ao conectar!'

        tela_login.destroy()
        info_cliente = resposta_login[1]
        __criar_tela_principal(info_cliente[0], info_rg, info_cliente[1])
    except Exception as e:
        print(e)
        __mostrar_janela_erro(e)

        

def __criar_janela_cadastro():
    try:
        global tela_cadastro
        tela_cadastro = tk.Toplevel(tela_inicio)
        tela_cadastro.title('Cadastro')
        tela_cadastro.geometry('300x250')

        nome = tk.StringVar()
        rg = tk.StringVar()
        pin = tk.StringVar()

        tk.Label(tela_cadastro, text="Insira as informações requisitadas", bg="blue", fg='white').pack()
        tk.Label(tela_cadastro, text="").pack()

        nome_lbl = tk.Label(tela_cadastro, text='Nome *')
        nome_lbl.pack()

        global nome_ent_cadastro
        nome_ent_cadastro = tk.Entry(tela_cadastro, textvariable=nome)
        nome_ent_cadastro.pack()

        rg_lbl = tk.Label(tela_cadastro, text='RG *')
        rg_lbl.pack()

        global rg_ent_cadastro
        rg_ent_cadastro = tk.Entry(tela_cadastro, textvariable=rg)
        rg_ent_cadastro.pack()

        global pin_ent_cadastro
        pin_lbl = tk.Label(tela_cadastro, text='PIN *')
        pin_lbl.pack()

        pin_ent_cadastro = tk.Entry(tela_cadastro, show='*',textvariable=pin)
        pin_ent_cadastro.pack()


        tk.Label(tela_cadastro, text="").pack()

        cadastro_btn = tk.Button(tela_cadastro, text='Confirmar', height='2', width='30', command=__cadastrar_usuario)
        cadastro_btn.pack()
    except Exception as e:
        print(e)
        __mostrar_janela_erro(e)

def __cadastrar_usuario():
    try:
        info_nome = nome_ent_cadastro.get()
        info_rg = rg_ent_cadastro.get()
        info_pin = pin_ent_cadastro.get()
        
        assert enviar_request_cadastro(info_nome, info_rg, info_pin), 'Erro ao cadastrar!'
           
        __mostrar_janela_sucesso('Usuário foi cadastrado!')
        
        tela_cadastro.destroy()
    except Exception as e:
        print(e)
        __mostrar_janela_erro(e)


def __mostrar_janela_transferir():
    try:
        resposta_obter_clientes = obter_lista_clientes()

        assert resposta_obter_clientes[0], "Erro ao carregar lista dos clientes. Por favor, tente novamente."
        # TODO : Tratar os dados para ser um array de rg - nome
        clientes = []

        tela_transferir = tk.Toplevel()
        tela_transferir.title('Transferir')

        frm_principal = tk.Frame(tela_transferir)

        transferir_cliente_selecionado = StringVar()
        transferir_cliente_selecionado_optionMenu = tk.OptionMenu(frm_principal, transferir_cliente_selecionado, clientes)

        transferir_valor = tk.Entry(frm_principal)
        transferir_btn = tk.Button(frm_principal, 
                                text='Transferir', 
                                height='2', 
                                width='10', 
                                bg='green', 
                                command=lambda: 
                                        __transferir(transferir_valor.get(), 
                                                    transferir_cliente_selecionado.get()))                               

        frm_principal.pack()
        transferir_cliente_selecionado_optionMenu.pack()    
        transferir_valor.pack()
        transferir_btn.pack()
    except Exception as e:
        print(e)
        __mostrar_janela_erro(e)

def __transferir(valor, clienteSelecionado):
    try:
        obter_lista_clientes()
    except Exception as e:
        print(e)
        __mostrar_janela_erro(e)

def __mostrar_tela_retirar(rg):
    try:
        tela_retirar = tk.Toplevel()
        tela_retirar.title('Retirada')

        tk.Label(tela_retirar, text='Insira o valor a ser sacado:', bg='blue', fg='white').pack()
        tk.Label(tela_retirar, text='').pack()

        global ent_valor_a_retirar
        ent_valor_a_retirar = tk.Entry(tela_retirar)

        ent_valor_a_retirar.pack()

        tk.Label(tela_retirar, text='').pack()

        retirar_btn = tk.Button(tela_retirar, text='Confirmar', height='2', width='10', command=lambda: enviar_request_saque(ent_valor_a_retirar.get(), rg))
        retirar_btn.pack()
    except Exception as e:
        print(e)
        __mostrar_janela_erro(e)

# Utilitários
def __mostrar_janela_erro(mensagem):
    messagebox.showerror(title='Erro!', message=mensagem)

def __mostrar_janela_sucesso(mensagem):
    messagebox.showinfo(title='Sucesso!', message=mensagem)