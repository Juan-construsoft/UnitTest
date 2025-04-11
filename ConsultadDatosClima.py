# consultar_datos.py
import sqlite3

def mostrar_datos():
    conn = sqlite3.connect("datos.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT ciudad, pais, temperatura, viento
        FROM datos
        ORDER BY id DESC
        LIMIT 10
    """)

    registros = cursor.fetchall()
    conn.close()

    if not registros:
        print("No hay datos almacenados todavía.")
    else:
        print("\nÚltimos registros almacenados:\n")
        for ciudad, pais, temp, viento in registros:
            print(f"Ciudad: {ciudad}, País: {pais}, Temperatura: {temp}°C, Viento: {viento} km/h")

if __name__ == "__main__":
    mostrar_datos()
