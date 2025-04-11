import pytest
from orden import calcular_total

def test_calcular_total_valido():
    items = [{'precio': 10, 'cantidad': 2}, {'precio': 5, 'cantidad': 3}]
    assert calcular_total(items) == 35.0

def test_calcular_total_decimales():
    items = [{'precio': 10.55, 'cantidad': 2}, {'precio': 5.25, 'cantidad': 3}]
    assert calcular_total(items) == 36.85

def test_calcular_total_un_item():
    items = [{'precio': 100, 'cantidad': 1}]
    assert calcular_total(items) == 100.0

def test_calcular_total_sin_items():
    with pytest.raises(ValueError, match="La orden debe ser una lista de ítems."):
        calcular_total(None)

def test_calcular_total_item_invalido():
    with pytest.raises(ValueError, match="Cada ítem debe tener 'precio' y 'cantidad'."):
        calcular_total([{'precio': 10}])

def test_calcular_total_precio_invalido():
    with pytest.raises(ValueError, match="El precio debe ser un número positivo."):
        calcular_total([{'precio': -10, 'cantidad': 2}])

def test_calcular_total_cantidad_invalida():
    with pytest.raises(ValueError, match="La cantidad debe ser un entero mayor a cero."):
        calcular_total([{'precio': 10, 'cantidad': 0}])