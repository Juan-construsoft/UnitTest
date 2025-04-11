# backend/db/database.py

import sqlite3
from pathlib import Path

# Ruta donde se almacenará la base de datos SQLite (archivo local "ecommerce.db")
DB_FILE = Path(__file__).resolve().parent / "ecommerce.db"

class Database:
    """
    Clase encargada de manejar la conexión a la base de datos SQLite.
    """

    def __init__(self):
        self.init_db()

    def connect(self):
        return sqlite3.connect(str(DB_FILE), check_same_thread=False)

    def close(self, connection):
        if connection:
            connection.close()

    def init_db(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()
