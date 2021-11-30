import tkinter as tk

def init_gui(nome, cpf, saldo):
    window = tk.Tk("Banco")
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

def transferir():
    pass

def retirar():
    pass