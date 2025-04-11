# test_cliente.py

import pytest
from cliente import Cliente

def test_validar_id_correcto():
    """
    Prueba que un ID válido sea aceptado.
    """
    try:
        Cliente.validar_id(1)
    except ValueError:
        pytest.fail("El ID es válido, pero se lanzó una excepción.")

def test_validar_id_invalido():
    """
    Prueba que se lance una excepción si el ID es inválido.
    """
    with pytest.raises(ValueError, match="El ID debe ser un número entero positivo."):
        Cliente.validar_id(-5)

def test_validar_nombre_apellido_correcto():
    """
    Prueba que un nombre/apellido válido sea aceptado.
    """
    try:
        Cliente.validar_nombre_apellido("Juan", "nombre")
    except ValueError:
        pytest.fail("El nombre es válido, pero se lanzó una excepción.")

def test_validar_nombre_apellido_vacio():
    """
    Prueba que se lance una excepción si el nombre/apellido está vacío.
    """
    with pytest.raises(ValueError, match="El nombre no puede estar vacío ni ser nulo."):
        Cliente.validar_nombre_apellido("", "nombre")

def test_validar_correo_correcto():
    """
    Prueba que un correo válido sea aceptado.
    """
    try:
        Cliente.validar_correo("juan@example.com")
    except ValueError:
        pytest.fail("El correo es válido, pero se lanzó una excepción.")

def test_validar_correo_invalido():
    """
    Prueba que se lance una excepción si el correo tiene un formato inválido.
    """
    with pytest.raises(ValueError, match="El correo electrónico no tiene un formato válido."):
        Cliente.validar_correo("correo-invalido")

def test_validar_edad_correcta():
    """
    Prueba que una edad válida sea aceptada.
    """
    try:
        Cliente.validar_edad(25)
    except ValueError:
        pytest.fail("La edad es válida, pero se lanzó una excepción.")

def test_validar_edad_menor_a_18():
    """
    Prueba que se lance una excepción si la edad es menor a 18.
    """
    with pytest.raises(ValueError, match="La edad debe ser un número entero entre 18 y 99 años."):
        Cliente.validar_edad(17)

def test_validar_edad_mayor_o_igual_a_100():
    """
    Prueba que se lance una excepción si la edad es mayor o igual a 100.
    """
    with pytest.raises(ValueError, match="La edad debe ser un número entero entre 18 y 99 años."):
        Cliente.validar_edad(100)

def test_validar_activo_correcto():
    """
    Prueba que un valor válido para 'activo' sea aceptado.
    """
    try:
        Cliente.validar_activo("si")
    except ValueError:
        pytest.fail("El valor de 'activo' es válido, pero se lanzó una excepción.")

def test_validar_activo_invalido():
    """
    Prueba que se lance una excepción si el valor de 'activo' es inválido.
    """
    with pytest.raises(ValueError, match="El campo 'activo' debe ser 'si' o 'no'."):
        Cliente.validar_activo("tal vez")