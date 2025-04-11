import pytest
from unittest.mock import MagicMock
from ordenBD import crear_orden

def test_crear_orden_exitosa():
    # 1. Mock del repositorio
    repo_mock = MagicMock()
    
    # 2. Simulamos cliente activo
    repo_mock.obtener_cliente_por_id.return_value = {
        "id": 1,
        "nombre": "Pipe",
        "activo": True
    }

    # 3. Simulamos guardar_orden (no hace nada)
    repo_mock.guardar_orden.return_value = None

    items = [{"precio": 1000, "cantidad": 2}]
    
    # 4. Ejecutar función
    resultado = crear_orden(1, items, repo_mock)

    # 5. Verificar resultados
    assert resultado == "Orden creada para Pipe, total: $2000"
    repo_mock.guardar_orden.assert_called_once()  # Verificamos que se haya llamado

def test_cliente_inexistente():
    repo_mock = MagicMock()
    repo_mock.obtener_cliente_por_id.return_value = None
    items = [{"precio": 500, "cantidad": 1}]
    
    with pytest.raises(ValueError, match="Cliente no encontrado"):
        crear_orden(999, items, repo_mock)

def test_cliente_inactivo():
    repo_mock = MagicMock()
    repo_mock.obtener_cliente_por_id.return_value = {
        "id": 2,
        "nombre": "Carlos",
        "activo": False
    }
    items = [{"precio": 200, "cantidad": 3}]
    
    with pytest.raises(ValueError, match="Cliente inactivo"):
        crear_orden(2, items, repo_mock)