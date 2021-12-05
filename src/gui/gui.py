from tkinter import messagebox, StringVar
from models.cliente import Cliente
from db.database import criar_cliente, autenticar_cliente, get_nome_cliente
import tkinter as tk
import sys, os
from tkinter.messagebox import *

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

WINDOW_DIMENSIONS = '300x250'

from client_module.client_layer import *

# TODO : Revisar variáveis globais
def __criar_janela_principal(nome, rg, saldo):
    try:        
        tela_principal, frm_principal = __criar_janela(titulo='Área principal', adicionarLabel=True, principal=True)
        frm_sub = tk.Frame(master=frm_principal, relief=tk.RIDGE, borderwidth=5)

        # Criar submenu a esquerda com nome, rg e saldo
        frm_menu = tk.Frame(master=frm_sub, relief=tk.RIDGE, borderwidth=5)
        lbl_dados = tk.Label(master=frm_menu, text="Dados do cliente")
        lbl_nome = tk.Label(master=frm_menu, text="Nome: " + nome)
        lbl_rg = tk.Label(master=frm_menu, text= "rg: " + rg)
        
        global saldo_atual
        saldo_atual = saldo
        lbl_saldo = tk.Label(master=frm_menu, text="Saldo: " + str(saldo_atual))

        # Criar submenu a direita com botões para transferir e realizar saque
        btn_transferir = tk.Button(master=frm_sub, text="Transferencia", command=lambda: __mostrar_janela_transferir(rg))
        saque_botao = tk.Button(master=frm_sub, text="Saque", command=lambda: __mostrar_tela_saque(rg))
        deposito_botao = tk.Button(master=frm_sub, text="Depósito", command=lambda: __mostrar_tela_deposito(rg))

        btn_transferir.pack(side=tk.RIGHT)
        saque_botao.pack(side=tk.RIGHT)
        deposito_botao.pack(side=tk.RIGHT)
        lbl_dados.pack()
        lbl_nome.pack()
        lbl_rg.pack()
        lbl_saldo.pack()
        frm_menu.pack(side=tk.LEFT, padx=5, pady=5)

        frm_sub.pack()
        frm_principal.pack(side=tk.TOP)

        # Fecha a tela de login/cadastro
        tela_inicio.destroy()

        # Definir nova principal
        tela_principal.mainloop()        
    except Exception as e:
        print(e)
        __mostrar_janela_erro(e)

def criar_janela_inicio():
    try:
        global tela_inicio
        tela_inicio, frm_prinicpal = __criar_janela(titulo='Login', adicionarLabel=True, principal=True)
        
        login_botao = tk.Button(master=frm_prinicpal, text='Login', height='2', width='30', command=__criar_janela_login)
        cadastrar_botao = tk.Button(master=frm_prinicpal, text='Cadastrar', height='2', width='30', command=__criar_janela_cadastro)

        # Construção da página
        frm_prinicpal.pack()
        tk.Label(master=frm_prinicpal, text='').pack()
        login_botao.pack()
        tk.Label(master=frm_prinicpal, text='').pack()
        cadastrar_botao.pack()
        tk.Label(master=frm_prinicpal, text='').pack()

        # Janela principal
        tela_inicio.mainloop()
    except Exception as e:
        print(e)
        __mostrar_janela_erro(e)

def __criar_janela_login():
    try:
        global tela_login
        tela_login, frm_principal = __criar_janela(titulo='Realizar login', adicionarLabel=False)

        global rg_verificar
        global pin_verificar
        rg_verificar = tk.StringVar()
        pin_verificar = tk.StringVar()

        # Header da janela
        tk.Label(frm_principal, text="Insira suas credenciais", bg="blue", fg='white').pack()
        tk.Label(frm_principal, text="").pack()

        # Input do RG
        global rg_ent_login
        rg_lbl = tk.Label(frm_principal, text='RG *')
        rg_ent_login = tk.Entry(frm_principal, textvariable=rg_verificar)

        # Input do PIN
        global pin_ent_login
        pin_lbl = tk.Label(frm_principal, text='PIN *')
        pin_ent_login = tk.Entry(frm_principal, show='*', textvariable=pin_verificar)

        # Botão de login
        login_botao = tk.Button(frm_principal, text='Login', height='2', width='30', command=__realizar_login)

        # Construção da página
        frm_principal.pack()
        rg_lbl.pack()
        rg_ent_login.pack()
        pin_lbl.pack()
        pin_ent_login.pack()
        tk.Label(frm_principal, text="").pack()
        login_botao.pack()
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
        __criar_janela_principal(info_cliente[0], info_rg, info_cliente[1])
    except Exception as e:
        print(e)
        __mostrar_janela_erro(e)

def __criar_janela_cadastro():
    try:
        global tela_cadastro
        tela_cadastro, frm_principal = __criar_janela(titulo='Cadastro', adicionarLabel=False)

        nome = tk.StringVar()
        rg = tk.StringVar()
        pin = tk.StringVar()

        tk.Label(frm_principal, text="Insira as informações requisitadas", bg="blue", fg='white').pack()

        # Input nome
        global nome_ent_cadastro
        nome_lbl = tk.Label(frm_principal, text='Nome *')
        nome_ent_cadastro = tk.Entry(frm_principal, textvariable=nome)

        # Input RG
        global rg_ent_cadastro
        rg_lbl = tk.Label(frm_principal, text='RG *')
        rg_ent_cadastro = tk.Entry(frm_principal, textvariable=rg)

        # Input Pin
        global pin_ent_cadastro
        pin_lbl = tk.Label(frm_principal, text='PIN *')
        pin_ent_cadastro = tk.Entry(frm_principal, show='*',textvariable=pin)

        # Botão cadastro
        cadastrar_botao = tk.Button(frm_principal, text='Confirmar', height='2', width='30', command=__cadastrar_usuario)

        # Construção da página
        frm_principal.pack()
        nome_lbl.pack()
        nome_ent_cadastro.pack()
        rg_lbl.pack()
        rg_ent_cadastro.pack()
        pin_lbl.pack()
        pin_ent_cadastro.pack()
        tk.Label(frm_principal, text="").pack()
        cadastrar_botao.pack()

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

def __mostrar_janela_transferir(rg):
    try:
        resposta_obter_clientes = obter_lista_clientes()

        assert resposta_obter_clientes[0], "Erro ao carregar lista dos clientes. Por favor, tente novamente."
        clientes = resposta_obter_clientes[1]

        # Removendo o cliente que é o próximo que está logado
        clientes = [cliente for cliente in clientes if not rg in cliente]

        _, frm_principal = __criar_janela(titulo='Transferir', adicionarLabel=False)

        # Dropdown para selecionar o cliente que receberá o valor
        transferir_cliente_selecionado = StringVar(frm_principal)
        transferir_cliente_selecionado.set('Selecione um cliente')
        transferir_cliente_selecionado_optionMenu = tk.OptionMenu(frm_principal, transferir_cliente_selecionado, *clientes)

        # Input para transferir o valor
        transferir_valor_lbl = tk.Label(master=frm_principal, text="Valor para transferência (R$)")
        transferir_valor = tk.Entry(frm_principal)
        transferir_botao = tk.Button(frm_principal, 
                                text='Transferir', 
                                height='2', 
                                width='10', 
                                bg='green', 
                                command=lambda: 
                                        __transferir(rg,
                                                    transferir_valor.get(), 
                                                    transferir_cliente_selecionado.get()))                               

        # Construção da página
        frm_principal.pack()
        transferir_cliente_selecionado_optionMenu.pack()    
        tk.Label(master=frm_principal, text='').pack()
        transferir_valor_lbl.pack()
        transferir_valor.pack()
        tk.Label(master=frm_principal, text='').pack()
        transferir_botao.pack()
    except Exception as e:
        print(e)
        __mostrar_janela_erro(e)

def __transferir(rg, valor, clienteSelecionado):
    try:
        pass
    except Exception as e:
        print(e)
        __mostrar_janela_erro(e)

def __mostrar_tela_saque(rg):
    try:
        _, frm_principal = __criar_janela(titulo='Saque', adicionarLabel=False)

        # Cabeçalho da janela
        info_label = tk.Label(master=frm_principal, text='Insira o valor a ser sacado:', bg='blue', fg='white')

        # Input valor para realizar saque
        global ent_valor_para_saque
        valor_lbl = tk.Label(master=frm_principal, text='Valor')
        ent_valor_para_saque = tk.Entry(frm_principal)

        # Botão realizar saque
        saque_botao = tk.Button(master=frm_principal, text='Confirmar', height='2', width='10', command=lambda: enviar_request_saque(ent_valor_para_saque.get(), rg))

        # Construção da página
        frm_principal.pack()
        info_label.pack()
        tk.Label(master=frm_principal, text='').pack()
        valor_lbl.pack()
        ent_valor_para_saque.pack()
        tk.Label(master=frm_principal, text='').pack()
        saque_botao.pack()

    except Exception as e:
        print(e)
        __mostrar_janela_erro(e)

def __mostrar_tela_deposito(rg):
    try:
        global tela_deposito
        tela_deposito, frm_principal = __criar_janela(titulo='Depósito', adicionarLabel=False)

        # Cabeçalho da janela
        info_label = tk.Label(master=frm_principal, text='Insira o valor a ser depositado:', bg='blue', fg='white')

        # Input valor para depósito
        valor_lbl = tk.Label(master=frm_principal, text='Valor')
        ent_valor_para_deposito = tk.Entry(frm_principal)

        # Botão realizar depósito
        deposito_botao = tk.Button(master=frm_principal, text='Confirmar', height='2', width='10', command=lambda: __realizar_deposito(ent_valor_para_deposito.get(), rg))

        # Construção da página
        frm_principal.pack()
        info_label.pack()
        tk.Label(master=frm_principal, text='').pack()
        valor_lbl.pack()
        ent_valor_para_deposito.pack()
        tk.Label(master=frm_principal, text='').pack()
        deposito_botao.pack()

    except Exception as e:
        print(e)
        __mostrar_janela_erro(e)

def __realizar_deposito(valor, rg):
    try:
        resposta = enviar_request_deposito(valor, rg)
        status = resposta[0]

        if status != Responses.SUCCESS:
            mensagem = resposta[1]
            if status == Responses.INTERNAL_ERROR:
                raise ValueError(mensagem)
            elif status == Responses.FORBIDDEN:
                __mostrar_janela_alerta(mensagem)
        else:
            __mostrar_janela_sucesso('Depósito realizado com sucesso!')
            tela_deposito.destroy()
            

    except Exception as e:
        print(e)
        __mostrar_janela_erro(e)

# Utilitários
def __atualizar_saldo(novoSaldo):
    saldo_atual = novoSaldo

def __mostrar_janela_erro(mensagem):
    messagebox.showerror(title='Erro!', message=mensagem)

def __mostrar_janela_sucesso(mensagem):
    messagebox.showinfo(title='Sucesso!', message=mensagem)

def __mostrar_janela_alerta(mensagem):
    messagebox.showwarning(title='Aviso', mensagem=mensagem)

def __criar_janela(titulo, adicionarLabel, principal = False):
    if principal:
        tela = tk.Tk()
    else:
        tela = tk.Toplevel()
        
    tela.title(titulo)
    tela.geometry(WINDOW_DIMENSIONS)
    tela.resizable(height=None, width=None)

    frm_principal = tk.Frame(tela)
    
    if adicionarLabel:
        __criar_label_padrao(frm_principal)

    return (tela, frm_principal)

def __criar_label_padrao(frameMaster):
    tk.Label(frameMaster, text="Banco do Bruhsil", bg="blue", width="300", height="2", font=("Calibri", 13), fg='white').pack()