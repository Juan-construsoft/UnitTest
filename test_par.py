import pytest
from EsPar  import es_par  # Asegúrate de importar la función correctamente

def test_es_par():
    assert es_par(4) == True  # Caso normal
    assert es_par(7) == False  # Caso normal
    assert es_par(0) == True  # El cero es par
    assert es_par(-2) == True  # Números negativos pares
    assert es_par(-3) == False  # Números negativos impares
    assert es_par(1001) == False  # Un número impar más grande