import pytest
from unittest.mock import patch
import requests

def get_data_from_api(url):
    response = requests.get(url)
    return response.json()

@patch('requests.get')
def test_get_data_from_api(mock_get):
    # Simular la respuesta de la API
    mock_get.return_value.json.return_value = {'key': 'value'}
    
    # Probar la función con el mock
    result = get_data_from_api('http://api.example.com/data')
    assert result == {'key': 'value'}