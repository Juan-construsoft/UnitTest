# backend/db/create_tables.py

from database import Database

def create_tables():
    db = Database()
    conn = db.connect()
    cursor = conn.cursor()

    # Tabla de usuarios
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # Tabla de productos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            discount REAL DEFAULT 0,
            stock INTEGER NOT NULL
        )
    """)

    # Tabla de carritos (1 carrito por usuario a modo simplificado)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS carts (
            cart_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)

    # Tabla intermedia cart_items (relación N a M entre carrito y productos)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cart_items (
            cart_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            cart_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 1,
            FOREIGN KEY (cart_id) REFERENCES carts(cart_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )
    """)

    conn.commit()
    db.close()
    print("Tablas creadas o verificadas correctamente.")

if __name__ == "__main__":
    create_tables()