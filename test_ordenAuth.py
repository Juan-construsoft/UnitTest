import pytest
from unittest.mock import MagicMock
from OrdenAuth import crear_orden

def test_crear_orden_con_autenticacion_valida():
    # Mocks
    auth_mock = MagicMock()
    repo_mock = MagicMock()

    # Token y resultado simulado
    token = "token_valido_123"
    auth_mock.validar_token_y_extraer_id.return_value = 1

    repo_mock.obtener_cliente_por_id.return_value = {
        "id": 1,
        "nombre": "Pipe",
        "activo": True
    }

    repo_mock.guardar_orden.return_value = None

    items = [{"precio": 1500, "cantidad": 2}]

    resultado = crear_orden(token, items, auth_mock, repo_mock)

    assert resultado == "Orden creada para Pipe, total: $3000"
    auth_mock.validar_token_y_extraer_id.assert_called_once_with(token)
    repo_mock.guardar_orden.assert_called_once()

def test_token_invalido():
    auth_mock = MagicMock()
    repo_mock = MagicMock()

    auth_mock.validar_token_y_extraer_id.return_value = None

    items = [{"precio": 1000, "cantidad": 1}]
    token = "token_invalido"

    with pytest.raises(ValueError, match="Token inválido"):
        crear_orden(token, items, auth_mock, repo_mock)

def test_cliente_inactivo_con_token_valido():
    auth_mock = MagicMock()
    repo_mock = MagicMock()

    auth_mock.validar_token_y_extraer_id.return_value = 2
    repo_mock.obtener_cliente_por_id.return_value = {
        "id": 2,
        "nombre": "Ana",
        "activo": False
    }

    items = [{"precio": 500, "cantidad": 2}]
    token = "token_valido"

    with pytest.raises(ValueError, match="Cliente inactivo"):
        crear_orden(token, items, auth_mock, repo_mock)