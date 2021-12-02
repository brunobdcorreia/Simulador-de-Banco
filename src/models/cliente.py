class Cliente:
    def __init__(self, nome, rg, pin, saldo=0):
        self.nome = nome
        self.rg = rg
        self.pin = pin
        self.saldo = saldo

    def get_nome(self):
        return self.nome

    def get_rg(self):
        return self.rg

    def get_pin(self):
        return self.pin

    def get_saldo(self):
        return self.saldo