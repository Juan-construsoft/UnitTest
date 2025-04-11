# backend/db/create_purchase_tables.py

from database import Database

def create_purchase_tables():
    db = Database()
    conn = db.connect()
    cursor = conn.cursor()

    # Tabla de compras (purchases)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS purchases (
            purchase_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            total_amount REAL NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)

    # Tabla de items de compra (purchase_items)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS purchase_items (
            purchase_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            purchase_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            price_at_purchase REAL NOT NULL,
            FOREIGN KEY (purchase_id) REFERENCES purchases(purchase_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )
    """)

    conn.commit()
    conn.close()