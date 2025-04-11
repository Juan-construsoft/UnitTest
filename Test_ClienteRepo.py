# test_cliente_repo.py
import pytest
from unittest.mock import patch, MagicMock
from ClienteRepo import obtener_cliente_por_id

@patch("ClienteRepo.sqlite3.connect")
def test_obtener_cliente_existente(mock_connect):
    # Simula el cursor y su resultado
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = (1, "Pipe", 1)
    mock_conn.cursor.return_value = mock_cursor
    mock_connect.return_value = mock_conn

    cliente = obtener_cliente_por_id(1)

    assert cliente == {
        "id": 1,
        "nombre": "Pipe",
        "activo": True
    }

@patch("ClienteRepo.sqlite3.connect")
def test_cliente_no_encontrado(mock_connect):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = None
    mock_conn.cursor.return_value = mock_cursor
    mock_connect.return_value = mock_conn

    cliente = obtener_cliente_por_id(999)

    assert cliente is None