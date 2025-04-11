# test_cliente_mod.py

import pytest
from cliente import Cliente, ClienteDB

#########################
# Tests para la clase Cliente
#########################

def test_crear_cliente_ok():
    """
    Verifica la creación exitosa de un cliente con datos válidos.
    """
    c = Cliente(
        id=1,
        nombre="Juan",
        apellido="Pérez",
        correo="juan.perez@example.com",
        edad=30,
        activo="si"
    )
    assert c.id == 1
    assert c.nombre == "Juan"
    assert c.apellido == "Pérez"
    assert c.correo == "juan.perez@example.com"
    assert c.edad == 30
    assert c.activo == "si"

def test_crear_cliente_id_invalido():
    """
    Verifica que se lance ValueError si el id es <= 0.
    """
    with pytest.raises(ValueError) as exc:
        Cliente(
            id=0,
            nombre="Pedro",
            apellido="López",
            correo="pedro@example.com",
            edad=25,
            activo="si"
        )
    assert "El ID debe ser un número entero positivo" in str(exc.value)

def test_crear_cliente_nombre_vacio():
    """
    Verifica que se lance ValueError si el nombre está vacío o en blanco.
    """
    with pytest.raises(ValueError) as exc:
        Cliente(
            id=1,
            nombre="",
            apellido="López",
            correo="pedro@example.com",
            edad=25,
            activo="si"
        )
    assert "no puede estar vacío ni ser nulo" in str(exc.value).lower()

def test_crear_cliente_correo_invalido():
    """
    Verifica que se lance ValueError con un email en formato inválido.
    """
    with pytest.raises(ValueError) as exc:
        Cliente(
            id=2,
            nombre="Ana",
            apellido="García",
            correo="correo-invalido",
            edad=22,
            activo="si"
        )
    assert "no tiene un formato válido" in str(exc.value).lower()

def test_crear_cliente_edad_invalida():
    """
    Verifica que se lance ValueError si la edad es < 18 o >= 100.
    """
    # Edad menor a 18
    with pytest.raises(ValueError) as exc_menor:
        Cliente(
            id=3,
            nombre="Carlos",
            apellido="Torres",
            correo="carlos@example.com",
            edad=17,
            activo="si"
        )
    assert "entre 18 y 99 años" in str(exc_menor.value)

    # Edad mayor o igual a 100
    with pytest.raises(ValueError) as exc_mayor:
        Cliente(
            id=4,
            nombre="Carmen",
            apellido="Ruiz",
            correo="carmen@example.com",
            edad=100,
            activo="si"
        )
    assert "entre 18 y 99 años" in str(exc_mayor.value)

def test_crear_cliente_activo_invalido():
    """
    Verifica que se lance ValueError si 'activo' no es 'si' ni 'no'.
    """
    with pytest.raises(ValueError) as exc:
        Cliente(
            id=5,
            nombre="Luis",
            apellido="Martínez",
            correo="luis@example.com",
            edad=28,
            activo="tal vez"
        )
    assert "debe ser 'si' o 'no'" in str(exc.value).lower()

def test_repr_cliente():
    """
    Cubre el método __repr__ para asegurar su funcionamiento.
    """
    c = Cliente(
        id=10,
        nombre="Test",
        apellido="User",
        correo="test.user@example.com",
        edad=29,
        activo="no"
    )
    salida_repr = repr(c)
    assert "Cliente(id=10, nombre=Test" in salida_repr

#########################
# Tests para la clase ClienteDB
#########################

@pytest.fixture
def db_vacia():
    """
    Devuelve una instancia de ClienteDB recién creada (sin clientes).
    """
    return ClienteDB()

@pytest.fixture
def cliente_ok():
    """
    Devuelve un Cliente válido.
    """
    return Cliente(
        id=99,
        nombre="Maria",
        apellido="López",
        correo="maria.lopez@example.com",
        edad=35,
        activo="si"
    )

def test_agregar_cliente_ok(db_vacia, cliente_ok):
    """
    Verifica que se pueda agregar un cliente nuevo correctamente.
    """
    db_vacia.agregar_cliente(cliente_ok)
    # Comprobamos que ahora exista en la base simulada
    assert db_vacia.obtener_cliente_por_id(99) is not None

def test_agregar_cliente_duplicado(db_vacia, cliente_ok):
    """
    Verifica que agregar un cliente con un ID ya existente lance ValueError.
    """
    db_vacia.agregar_cliente(cliente_ok)
    with pytest.raises(ValueError) as exc:
        db_vacia.agregar_cliente(cliente_ok)
    assert "Ya existe un cliente con el ID 99" in str(exc.value)

def test_obtener_cliente_inexistente(db_vacia):
    """
    Verifica que obtener_cliente_por_id devuelva None 
    si el cliente no existe.
    """
    resultado = db_vacia.obtener_cliente_por_id(999)
    assert resultado is None

def test_actualizar_cliente_ok(db_vacia, cliente_ok):
    """
    Verifica la actualización correcta de campos válidos.
    """
    db_vacia.agregar_cliente(cliente_ok)
    db_vacia.actualizar_cliente(99, nombre="Maria del Carmen", activo="no")
    cliente_actualizado = db_vacia.obtener_cliente_por_id(99)
    assert cliente_actualizado.nombre == "Maria del Carmen"
    assert cliente_actualizado.activo == "no"

def test_actualizar_cliente_inexistente(db_vacia):
    """
    Verifica que se lance ValueError al intentar actualizar 
    un cliente que no existe.
    """
    with pytest.raises(ValueError) as exc:
        db_vacia.actualizar_cliente(123, nombre="Alguien")
    assert "No existe un cliente con el ID 123" in str(exc.value)

def test_actualizar_campo_invalido(db_vacia, cliente_ok):
    """
    Verifica que se lance ValueError si se intenta actualizar 
    un campo que no existe en la clase Cliente.
    """
    db_vacia.agregar_cliente(cliente_ok)
    with pytest.raises(ValueError) as exc:
        db_vacia.actualizar_cliente(99, genero="femenino")
    assert "El campo 'genero' no es válido" in str(exc.value)

def test_eliminar_cliente_ok(db_vacia, cliente_ok):
    """
    Verifica la eliminación de un cliente existente.
    """
    db_vacia.agregar_cliente(cliente_ok)
    db_vacia.eliminar_cliente(99)
    assert db_vacia.obtener_cliente_por_id(99) is None

def test_eliminar_cliente_inexistente(db_vacia):
    """
    Verifica que se lance ValueError al intentar eliminar 
    un cliente que no existe.
    """
    with pytest.raises(ValueError) as exc:
        db_vacia.eliminar_cliente(888)
    assert "No existe un cliente con el ID 888" in str(exc.value)

def test_listar_clientes(db_vacia, cliente_ok):
    """
    Verifica que se liste correctamente a los clientes agregados.
    """
    assert db_vacia.listar_clientes() == []
    db_vacia.agregar_cliente(cliente_ok)
    lista = db_vacia.listar_clientes()
    assert len(lista) == 1
    assert lista[0].nombre == "Maria"
