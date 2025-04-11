class CuentaBancaria:
    def __init__(self, titular, saldo_inicial=0):
        self.titular = titular
        self.saldo = saldo_inicial

    def consignar(self, monto):
        if monto > 0:
            self.saldo += monto
            return True
        return False

    def retirar(self, monto):
        if 0 < monto <= self.saldo:
            self.saldo -= monto
            return True
        return False

    def consultar_saldo(self):
        return self.saldo