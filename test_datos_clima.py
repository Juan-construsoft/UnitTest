# test_api_datos_clima_ubicacion.py
import pytest
from unittest.mock import patch, MagicMock
from DatosClima import ejecutar

@patch("DatosClima.almacenar_datos")
@patch("DatosClima.obtener_clima")
@patch("DatosClima.obtener_ubicacion")
def test_ejecutar_flujo_completo(mock_ubicacion, mock_clima, mock_almacenar):
    mock_ubicacion.return_value = {
        "ip": "123.45.67.89",
        "ciudad": "Bogotá",
        "pais": "Colombia"
    }

    mock_clima.return_value = {
        "temperatura": 18.5,
        "viento": 12.3
    }

    resultado = ejecutar()

    mock_almacenar.assert_called_once_with(mock_clima.return_value, mock_ubicacion.return_value)
    assert resultado == "Datos almacenados correctamente"

@patch("DatosClima.obtener_ubicacion")
def test_ejecutar_falla_por_datos_invalidos(mock_ubicacion):
    mock_ubicacion.return_value = None

    with pytest.raises(ValueError, match="Faltan datos para almacenar"):
        ejecutar()
