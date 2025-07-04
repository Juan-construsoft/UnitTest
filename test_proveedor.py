import pytest
from Proveedor import Proveedor, ProveedorDB


def test_crear_proveedor_ok():
    p = Proveedor(1, "ABC", "Calle 1", "Juan Perez", "abc@example.com", "1234")
    assert p.identificacion == 1
    assert p.nombre == "ABC"


def test_crear_proveedor_id_invalido():
    with pytest.raises(ValueError):
        Proveedor(0, "ABC", "Calle 1", "Juan Perez", "abc@example.com", "1234")


@pytest.fixture
def db_vacia():
    return ProveedorDB()


@pytest.fixture
def proveedor_ok():
    return Proveedor(2, "XYZ", "Calle 2", "Ana Lopez", "xyz@example.com", "5678")


def test_agregar_proveedor_ok(db_vacia, proveedor_ok):
    db_vacia.agregar_proveedor(proveedor_ok)
    assert db_vacia.obtener_proveedor_por_id(2) is not None


def test_agregar_proveedor_duplicado(db_vacia, proveedor_ok):
    db_vacia.agregar_proveedor(proveedor_ok)
    with pytest.raises(ValueError):
        db_vacia.agregar_proveedor(proveedor_ok)


def test_obtener_proveedor_inexistente(db_vacia):
    assert db_vacia.obtener_proveedor_por_id(99) is None


def test_actualizar_proveedor_ok(db_vacia, proveedor_ok):
    db_vacia.agregar_proveedor(proveedor_ok)
    db_vacia.actualizar_proveedor(2, nombre="XYZ2")
    assert db_vacia.obtener_proveedor_por_id(2).nombre == "XYZ2"


def test_actualizar_proveedor_inexistente(db_vacia):
    with pytest.raises(ValueError):
        db_vacia.actualizar_proveedor(3, nombre="No")


def test_eliminar_proveedor_ok(db_vacia, proveedor_ok):
    db_vacia.agregar_proveedor(proveedor_ok)
    db_vacia.eliminar_proveedor(2)
    assert db_vacia.obtener_proveedor_por_id(2) is None


def test_eliminar_proveedor_inexistente(db_vacia):
    with pytest.raises(ValueError):
        db_vacia.eliminar_proveedor(5)

