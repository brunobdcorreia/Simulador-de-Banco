from tkinter import messagebox
from models.cliente import Cliente
from db.database import criar_cliente
import tkinter as tk
from tkinter.messagebox import *
import os

def init_gui(nome, cpf, saldo):
    window = tk.Tk("Banco")
    window.title('Banco do Bruhsil')
    frm_main = tk.Frame()
    frm_sub = tk.Frame(master=frm_main, relief=tk.RIDGE, borderwidth=5)
    lbl_banco = tk.Label(master=frm_main, text="Banco do Bruhsil")

    # Criar submenu a esquerda com nome, cpf e saldo
    frm_menu = tk.Frame(master=frm_sub, relief=tk.RIDGE, borderwidth=5)
    lbl_dados = tk.Label(master=frm_menu, text="Dados do cliente")
    lbl_nome = tk.Label(master=frm_menu, text="Nome: " + nome)
    lbl_cpf = tk.Label(master=frm_menu, text= "CPF: " + cpf)
    lbl_saldo = tk.Label(master=frm_menu, text="Saldo: " + saldo)

    # Criar submenu a direita com botões para transferir e retirar
    btn_transferir = tk.Button(master=frm_sub, text="Realizar transferencia", command=transferir)
    btn_retirar = tk.Button(master=frm_sub, text="Retirar", command=retirar)

    btn_transferir.pack(side=tk.RIGHT)
    btn_retirar.pack(side=tk.RIGHT)
    lbl_dados.pack()
    lbl_nome.pack()
    lbl_cpf.pack()
    lbl_saldo.pack()
    frm_menu.pack(side=tk.LEFT, padx=5, pady=5)

    lbl_banco.pack()
    frm_sub.pack()
    frm_main.pack(side=tk.TOP)

    window.mainloop()

def criar_janela_inicio():
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

def __criar_janela_login():
    global tela_login
    tela_login = tk.Toplevel(tela_inicio)
    tela_login.title('Realizar login')
    tela_login.geometry('300x250')

    global usuario_verificar
    global rg_verificar

    usuario_verificar = tk.StringVar()
    rg_verificar = tk.StringVar()

    tk.Label(tela_login, text="Insira suas credenciais", bg="blue", fg='white').pack()
    tk.Label(tela_login, text="").pack()

    usuario_lbl = tk.Label(tela_login, text='Usuario *')
    usuario_lbl.pack()

    global usuario_ent_login
    usuario_ent_login = tk.Entry(tela_login, textvariable=usuario_verificar)
    usuario_ent_login.pack()

    rg_lbl = tk.Label(tela_login, text='RG *')
    rg_lbl.pack()

    global rg_ent_login
    rg_ent_login = tk.Entry(tela_login, textvariable=rg_verificar)
    rg_ent_login.pack()

    tk.Label(tela_login, text="").pack()

    login_btn = tk.Button(tela_login, text='Login', height='2', width='30', command=__realizar_login)
    login_btn.pack()


def __realizar_login():
    info_usuario = usuario_ent_login.get()
    info_rg = rg_ent_login.get()
    cliente = Cliente(info_usuario, info_rg)
    # Inserir bagulhos para logar cliente
    messagebox.showinfo(title='Login', message='Login feito com sucesso!')
    tela_login.destroy()

def __criar_janela_cadastro():
    global tela_cadastro
    tela_cadastro = tk.Toplevel(tela_inicio)
    tela_cadastro.title('Cadastro')
    tela_cadastro.geometry('300x250')

    nome = tk.StringVar()
    rg = tk.StringVar()

    tk.Label(tela_cadastro, text="Insira as informações requisitadas", bg="blue", fg='white').pack()
    tk.Label(tela_cadastro, text="").pack()

    usuario_lbl = tk.Label(tela_cadastro, text='Usuario *')
    usuario_lbl.pack()

    global usuario_ent_cadastro
    usuario_ent_cadastro = tk.Entry(tela_cadastro, textvariable=nome)
    usuario_ent_cadastro.pack()

    rg_lbl = tk.Label(tela_cadastro, text='RG *')
    rg_lbl.pack()

    global rg_ent_cadastro
    rg_ent_cadastro = tk.Entry(tela_cadastro, textvariable=rg)
    rg_ent_cadastro.pack()

    tk.Label(tela_cadastro, text="").pack()

    cadastro_btn = tk.Button(tela_cadastro, text='Confirmar', height='2', width='30', command=__cadastrar_usuario)
    cadastro_btn.pack()

def __cadastrar_usuario():
    info_usuario = usuario_ent_cadastro.get()
    info_rg = rg_ent_cadastro.get()
    cliente = Cliente(info_usuario, info_rg)
    criar_cliente(cliente)
    messagebox.showinfo(title='Cadastro confirmado', message='Cliente cadastrado com sucesso!')
    tela_cadastro.destroy()
    #tela_cadastro.update()

def transferir():
    pass

def retirar():
    pass