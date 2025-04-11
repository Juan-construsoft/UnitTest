import requests

def get_data_from_api(url):
    """
    Realiza una petición GET a la API y devuelve el JSON como diccionario.
    """
    response = requests.get(url)
    response.raise_for_status()  # Lanza error si la respuesta es 4xx o 5xx
    return response.json()

def consultar_precio_dolar(moneda_destino="COP"):
    """
    Consulta el valor del dólar en la moneda destino (por defecto COP).
    Retorna la tasa de cambio (float).
    """
    url = "https://api.exchangerate-api.com/v4/latest/USD"
    data = get_data_from_api(url)

    if moneda_destino not in data["rates"]:
        raise ValueError(f"La moneda '{moneda_destino}' no está disponible.")

    tasa = data["rates"][moneda_destino]
    return tasa

def convertir_monto(monto_usd, moneda_destino="COP"):
    """
    Convierte un monto en USD a la moneda destino.
    Imprime el resultado en consola.
    """
    tasa = consultar_precio_dolar(moneda_destino)
    convertido = monto_usd * tasa
    print(f"{monto_usd} USD equivale a {convertido:.2f} {moneda_destino}")
    return convertido

# ✅ Si ejecutas este archivo directamente:
if __name__ == "__main__":
    monto = float(input("Ingrese el monto en USD: "))
    moneda = input("Ingrese la moneda destino (por defecto COP): ").upper() or "COP"
    convertir_monto(monto, moneda)
