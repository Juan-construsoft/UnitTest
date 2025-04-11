# numeros.py

def es_primo(numero):
    """Retorna True si el número es primo, False en caso contrario."""
    if not isinstance(numero, int):
        raise ValueError("El número debe ser un entero.")
    if numero <= 1:
        return False
    for i in range(2, int(numero ** 0.5) + 1):
        if numero % i == 0:
            return False
    return True