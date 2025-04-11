import unittest
import requests
from unittest.mock import patch
from Conversor import get_data_from_api, consultar_precio_dolar, convertir_monto

class TestConversor(unittest.TestCase):
    def setUp(self):
        # Datos de prueba simulando respuesta exitosa de la API
        self.mock_api_data = {
            "result": "success",
            "base_code": "USD",
            "rates": {
                "COP": 3900.50,
                "EUR": 0.92,
                "MXN": 17.25,
                "JPY": 110.25,
                "GBP": 0.73
            },
            "time_last_update_utc": "2024-01-01 00:00:00 +0000"
        }
    self.api_url = 'https://api.exchangerate-api.com/v4/latest/USD'
        
        # Datos de prueba para simular diferentes tipos de respuestas de error
        self.mock_error_responses = {
            'not_found': {
                'error': 'Resource not found',
                'status_code': 404
            },
            'rate_limit': {
                'error': 'API rate limit exceeded',
                'status_code': 429
            },
            'server_error': {
                'error': 'Internal server error',
                'status_code': 500
            }
        }

    @patch('requests.get')
    def test_get_data_from_api(self, mock_get):
        # Configurar el mock para simular una respuesta exitosa
        mock_get.return_value.json.return_value = self.mock_api_data
        mock_get.return_value.raise_for_status.return_value = None

        # Probar la función
        result = get_data_from_api(self.api_url)
        self.assertEqual(result, self.mock_api_data)
        mock_get.assert_called_once_with(self.api_url)

    @patch('Conversor.get_data_from_api')
    def test_consultar_precio_dolar_moneda_valida(self, mock_get_data):
        # Configurar el mock
        mock_get_data.return_value = self.mock_api_data

        # Probar con diferentes monedas válidas
        self.assertEqual(consultar_precio_dolar('COP'), 3900.50)
        self.assertEqual(consultar_precio_dolar('EUR'), 0.92)
        self.assertEqual(consultar_precio_dolar('MXN'), 17.25)

    @patch('Conversor.get_data_from_api')
    def test_consultar_precio_dolar_moneda_invalida(self, mock_get_data):
        # Configurar el mock
        mock_get_data.return_value = self.mock_api_data

        # Probar con una moneda inválida
        with self.assertRaises(ValueError):
            consultar_precio_dolar('XXX')

    @patch('Conversor.consultar_precio_dolar')
    def test_convertir_monto(self, mock_consultar):
        # Configurar el mock
        mock_consultar.return_value = 3900.50

        # Probar la conversión
        resultado = convertir_monto(100, 'COP')
        self.assertEqual(resultado, 390050.0)

    @patch('requests.get')
    def test_error_api(self, mock_get):
        # Probar diferentes escenarios de error
        for error_type, error_data in self.mock_error_responses.items():
            with self.subTest(error_type=error_type):
                # Configurar el mock para simular la respuesta de error
                mock_response = requests.Response()
                mock_response.status_code = error_data['status_code']
                mock_response._content = str(error_data['error']).encode()
                mock_get.return_value = mock_response

                # La función raise_for_status() lanzará HTTPError
                with self.assertRaises(requests.HTTPError):
                    get_data_from_api(self.api_url)

        # Probar error de conexión
        mock_get.side_effect = requests.ConnectionError('No internet connection')
        with self.assertRaises(requests.ConnectionError):
            get_data_from_api(self.api_url)

        # Probar timeout
        mock_get.side_effect = requests.Timeout('Request timed out')
        with self.assertRaises(requests.Timeout):
            get_data_from_api(self.api_url)

if __name__ == '__main__':
    unittest.main()