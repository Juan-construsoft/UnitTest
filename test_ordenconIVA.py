import pytest
from ordenconIVA import calcular_total_con_iva

def test_total_colombia():
    items = [{"precio": 1000, "cantidad": 2}]
    assert calcular_total_con_iva(items, "Colombia") == 2380.0

def test_total_mexico():
    items = [{"precio": 1000, "cantidad": 2}]
    assert calcular_total_con_iva(items, "México") == 2320.0

def test_total_otros_paises():
    items = [{"precio": 1000, "cantidad": 2}]
    assert calcular_total_con_iva(items, "Ecuador") == 2000.0

def test_lista_vacia():
    assert calcular_total_con_iva([], "Colombia") == 0.0

def test_error_si_no_lista():
    with pytest.raises(ValueError):
        calcular_total_con_iva("cadena", "Colombia")

def test_error_sin_precio_o_cantidad():
    with pytest.raises(ValueError):
        calcular_total_con_iva([{"precio": 1000}], "Colombia")
