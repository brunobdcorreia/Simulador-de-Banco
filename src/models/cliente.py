class Cliente:
    def __init__(self, nome, rg, saldo=0):
        self.nome = nome
        self.rg = rg
        self.saldo = saldo

    def get_nome(self):
        return self.nome

    def get_rg(self):
        return self.rg

    def get_saldo(self):
        return self.saldo