# test_numeros.py

import pytest
from numeros import es_primo

def test_numeros_primos():
    assert es_primo(2) is True
    assert es_primo(3) is True
    assert es_primo(13) is True
    assert es_primo(97) is True

def test_numeros_no_primos():
    assert es_primo(1) is False
    assert es_primo(4) is False
    assert es_primo(100) is False
    assert es_primo(0) is False
    assert es_primo(-5) is False

def test_valores_invalidos():
    with pytest.raises(ValueError):
        es_primo(3.14)
    with pytest.raises(ValueError):
        es_primo("cinco")
    with pytest.raises(ValueError):
        es_primo(None)
