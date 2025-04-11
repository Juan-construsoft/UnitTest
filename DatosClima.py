# api_datos_clima_ubicacion.py
import requests
import sqlite3

def obtener_clima(ciudad):
    url = f"https://api.open-meteo.com/v1/forecast?latitude=4.61&longitude=-74.08&current_weather=true"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return {
        "temperatura": data["current_weather"]["temperature"],
        "viento": data["current_weather"]["windspeed"]
    }

def obtener_ubicacion():
    url = "https://ipapi.co/json"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return {
        "ip": data["ip"],
        "ciudad": data["city"],
        "pais": data["country_name"]
    }

def validar_datos(clima, ubicacion):
    if not clima or not ubicacion:
        raise ValueError("Faltan datos para almacenar")
    if "temperatura" not in clima or "ciudad" not in ubicacion:
        raise ValueError("Datos incompletos")
    return True

def almacenar_datos(clima, ubicacion):
    conn = sqlite3.connect("datos.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS datos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ciudad TEXT,
            pais TEXT,
            temperatura REAL,
            viento REAL
        )
    """)
    cursor.execute("""
        INSERT INTO datos (ciudad, pais, temperatura, viento)
        VALUES (?, ?, ?, ?)
    """, (
        ubicacion["ciudad"],
        ubicacion["pais"],
        clima["temperatura"],
        clima["viento"]
    ))
    conn.commit()
    conn.close()

def ejecutar():
    ubicacion = obtener_ubicacion()
    if not ubicacion:
        raise ValueError("Faltan datos para almacenar")
    clima = obtener_clima(ubicacion["ciudad"])
    if validar_datos(clima, ubicacion):
        almacenar_datos(clima, ubicacion)
        return "Datos almacenados correctamente"

if __name__ == "__main__":
    print(ejecutar())