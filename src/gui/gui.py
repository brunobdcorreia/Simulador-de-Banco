from models.cliente import Cliente
from db.database import criar_cliente
import tkinter as tk
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

def criar_janela_login():
    global tela_login
    tela_login = tk.Tk('Login')
    tela_login.geometry('300x250')
    tela_login.resizable(height=None, width=None)

    intro_lbl = tk.Label(text="Banco do Bruhsil", bg="blue", width="300", height="2", font=("Calibri", 13), fg='white').pack()
    tk.Label(text='').pack()
    login_btn = tk.Button(text='Login', height='2', width='30')
    login_btn.pack()
    tk.Label(text='').pack()

    register_btn = tk.Button(text='Cadastrar', height='2', width='30', command=criar_janela_cadastro)
    register_btn.pack()

    tela_login.mainloop()

def criar_janela_cadastro():
    tela_cadastro = tk.Toplevel(tela_login)
    tela_cadastro.title('Cadastro')
    tela_cadastro.geometry('300x250')

    nome = tk.StringVar()
    rg = tk.StringVar()

    tk.Label(tela_cadastro, text="Insira as informações requisitadas", bg="blue", fg='white').pack()
    tk.Label(tela_cadastro, text="").pack()

    usuario_lbl = tk.Label(tela_cadastro, text='Usuario *')
    usuario_lbl.pack()

    global usuario_ent
    usuario_ent = tk.Entry(tela_cadastro, textvariable=nome)
    usuario_ent.pack()

    rg_lbl = tk.Label(tela_cadastro, text='RG *')
    rg_lbl.pack()

    global rg_ent
    rg_ent = tk.Entry(tela_cadastro, textvariable=rg)
    rg_ent.pack()

    tk.Label(tela_cadastro, text="").pack()

    cadastro_btn = tk.Button(tela_cadastro, text='Confirmar', height='2', width='30', command=cadastrar_usuario)
    cadastro_btn.pack()

def cadastrar_usuario():
    info_usuario = usuario_ent.get()
    info_rg = rg_ent.get()
    cliente = Cliente(info_usuario, info_rg)
    criar_cliente(cliente)

def transferir():
    pass

def retirar():
    pass