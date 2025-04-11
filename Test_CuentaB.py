import pytest
from CuentaBanco import CuentaBancaria

def test_crear_cuenta():
    cuenta = CuentaBancaria("Juan", 1000)
    assert cuenta.titular == "Juan"
    assert cuenta.saldo == 1000

def test_crear_cuenta_sin_saldo_inicial():
    cuenta = CuentaBancaria("Maria")
    assert cuenta.titular == "Maria"
    assert cuenta.saldo == 0

def test_consignar_monto_valido():
    cuenta = CuentaBancaria("Pedro", 500)
    assert cuenta.consignar(200) == True
    assert cuenta.saldo == 700

def test_consignar_monto_invalido():
    cuenta = CuentaBancaria("Ana", 500)
    assert cuenta.consignar(-100) == False
    assert cuenta.saldo == 500
    assert cuenta.consignar(0) == False
    assert cuenta.saldo == 500

def test_retirar_monto_valido():
    cuenta = CuentaBancaria("Carlos", 1000)
    assert cuenta.retirar(500) == True
    assert cuenta.saldo == 500

def test_retirar_monto_mayor_al_saldo():
    cuenta = CuentaBancaria("Diana", 500)
    assert cuenta.retirar(600) == False
    assert cuenta.saldo == 500

def test_retirar_monto_invalido():
    cuenta = CuentaBancaria("Elena", 500)
    assert cuenta.retirar(-100) == False
    assert cuenta.saldo == 500
    assert cuenta.retirar(0) == False
    assert cuenta.saldo == 500

def test_consultar_saldo():
    cuenta = CuentaBancaria("Fernando", 750)
    assert cuenta.consultar_saldo() == 750