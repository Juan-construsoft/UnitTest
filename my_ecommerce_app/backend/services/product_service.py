# backend/services/product_service.py

import sys
sys.path.append('..')
from ..db.database import Database
from models.product import Product

class ProductService:
    def __init__(self):
        self.db = Database()

    def create_product(self, name, price, discount, stock):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO products (name, price, discount, stock)
            VALUES (?, ?, ?, ?)
        """, (name, price, discount, stock))
        conn.commit()
        return cursor.lastrowid

    def get_product_by_id(self, product_id):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT product_id, name, price, discount, stock FROM products WHERE product_id = ?", (product_id,))
        row = cursor.fetchone()
        if row:
            return Product(*row)
        return None

    def update_product_stock(self, product_id, new_stock):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE products
            SET stock = ?
            WHERE product_id = ?
        """, (new_stock, product_id))
        conn.commit()
        return cursor.rowcount  # 0 si no actualizó, 1 si sí

    def delete_product(self, product_id):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products WHERE product_id = ?", (product_id,))
        conn.commit()
        return cursor.rowcount

    def get_all_products(self):
        conn = None
        try:
            conn = self.db.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT product_id, name, price, discount, stock FROM products")
            rows = cursor.fetchall()
            return [Product(*row) for row in rows]
        except Exception as e:
            print(f"Error fetching products: {str(e)}")
            return []
        finally:
            if conn:
                self.db.close(conn)
