import pytest
from unittest.mock import patch, MagicMock
import requests
from Conversor import consultar_precio_dolar, convertir_monto, get_data_from_api

@pytest.fixture
def mock_api_response():
    return {
        "result": "success",
        "base_code": "USD",
        "rates": {
            "COP": 4000,
            "EUR": 0.92,
            "MXN": 17.25
        },
        "time_last_update_utc": "2024-01-01 00:00:00 +0000"
    }

@patch("Conversor.requests.get")
def test_conversion_exitosa(mock_get, mock_api_response):
    mock_get.return_value.json.return_value = mock_api_response
    mock_get.return_value.raise_for_status.return_value = None

    # Probar consulta de tasa de cambio
    resultado = consultar_precio_dolar("COP")
    assert resultado == 4000

    # Probar conversión de monto
    conversion = convertir_monto(10, "COP")
    assert conversion == 40000

    # Verificar que se llamó a la API con la URL correcta
    mock_get.assert_called_with("https://api.exchangerate-api.com/v4/latest/USD")

@patch("Conversor.requests.get")
def test_moneda_no_existente(mock_get, mock_api_response):
    mock_get.return_value.json.return_value = mock_api_response
    mock_get.return_value.raise_for_status.return_value = None

    with pytest.raises(ValueError, match="no está disponible"):
        consultar_precio_dolar("XXX")

@patch("Conversor.requests.get")
def test_sin_conexion_api(mock_get):
    mock_get.side_effect = requests.exceptions.ConnectionError("No hay conexión")

    with pytest.raises(requests.exceptions.ConnectionError, match="No hay conexión"):
        get_data_from_api("https://api.exchangerate-api.com/v4/latest/USD")

@patch("Conversor.requests.get")
def test_error_http(mock_get):
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("Error 500")
    mock_get.return_value = mock_response

    with pytest.raises(requests.exceptions.HTTPError, match="Error 500"):
        get_data_from_api("https://api.exchangerate-api.com/v4/latest/USD")

@patch("Conversor.requests.get")
def test_timeout_api(mock_get):
    mock_get.side_effect = requests.exceptions.Timeout("Tiempo de espera agotado")

    with pytest.raises(requests.exceptions.Timeout, match="Tiempo de espera agotado"):
        get_data_from_api("https://api.exchangerate-api.com/v4/latest/USD")