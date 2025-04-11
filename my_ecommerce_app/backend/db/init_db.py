# backend/db/init_db.py

from database import Database

def init_database():
    db = Database()
    conn = db.connect()
    cursor = conn.cursor()

    # Create products table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            discount REAL DEFAULT 0.0,
            stock INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_database()
    print('Database initialized successfully!')