# backend/services/cart_service.py

from ..db.database import Database
from ..models.cart import Cart
from ..models.product import Product

class CartService:
    def __init__(self):
        self.db = Database()

    def create_cart_for_user(self, user_id):
        """
        Crea un carrito vacío para un usuario si no lo tiene aún.
        """
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO carts (user_id) VALUES (?)
        """, (user_id,))
        conn.commit()
        return cursor.lastrowid

    def get_cart_by_user_id(self, user_id):
        """
        Retorna el primer carrito que encuentre para un user_id.
        (Simplificado: asume 1 carrito por usuario)
        """
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT cart_id, user_id FROM carts WHERE user_id = ?
        """, (user_id,))
        row = cursor.fetchone()
        if row:
            return Cart(*row)
        return None

    def add_product_to_cart(self, cart_id, product_id, quantity=1):
        """
        Agrega un producto al carrito (o incrementa la cantidad si ya existe).
        """
        conn = self.db.connect()
        cursor = conn.cursor()
        # Primero revisamos si el producto ya está en el carrito
        cursor.execute("""
            SELECT quantity FROM cart_items
            WHERE cart_id = ? AND product_id = ?
        """, (cart_id, product_id))
        row = cursor.fetchone()

        if row:
            new_qty = row[0] + quantity
            cursor.execute("""
                UPDATE cart_items
                SET quantity = ?
                WHERE cart_id = ? AND product_id = ?
            """, (new_qty, cart_id, product_id))
        else:
            cursor.execute("""
                INSERT INTO cart_items (cart_id, product_id, quantity)
                VALUES (?, ?, ?)
            """, (cart_id, product_id, quantity))

        conn.commit()

    def remove_product_from_cart(self, cart_id, product_id):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM cart_items
            WHERE cart_id = ? AND product_id = ?
        """, (cart_id, product_id))
        conn.commit()

    def get_cart_items(self, cart_id):
        """
        Devuelve una lista de tuplas (Product, quantity).
        """
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.product_id, p.name, p.price, p.discount, p.stock, ci.quantity
            FROM cart_items ci
            JOIN products p ON ci.product_id = p.product_id
            WHERE ci.cart_id = ?
        """, (cart_id,))
        rows = cursor.fetchall()

        results = []
        for r in rows:
            product = Product(r[0], r[1], r[2], r[3], r[4])
            quantity = r[5]
            results.append((product, quantity))
        return results

    def get_cart_total(self, cart_id):
        """
        Calcula el total a pagar del carrito (considerando descuentos).
        """
        items = self.get_cart_items(cart_id)
        total = 0.0
        for (product, qty) in items:
            total += product.get_final_price() * qty
        return total
