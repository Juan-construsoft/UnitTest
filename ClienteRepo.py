# cliente_repo.py
import sqlite3

def obtener_cliente_por_id(cliente_id):
    conn = sqlite3.connect("clientes.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nombre, activo
        FROM clientes
        WHERE id = ?
    """, (cliente_id,))

    resultado = cursor.fetchone()
    conn.close()

    if resultado:
        return {
            "id": resultado[0],
            "nombre": resultado[1],
            "activo": bool(resultado[2])
        }
    else:
        return None