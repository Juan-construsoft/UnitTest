# backend/services/purchase_service.py

from backend.db.database import Database
from backend.models.product import Product

class PurchaseService:
    def __init__(self):
        self.db = Database()

    def create_purchase(self, user_id, cart_items, total_amount):
        """
        Crea una nueva compra para el usuario con los items del carrito.
        """
        conn = self.db.connect()
        cursor = conn.cursor()
        
        try:
            # Crear la compra
            cursor.execute("""
                INSERT INTO purchases (user_id, total_amount)
                VALUES (?, ?)
            """, (user_id, total_amount))
            
            purchase_id = cursor.lastrowid
            
            # Insertar los items de la compra
            for product, quantity in cart_items:
                cursor.execute("""
                    INSERT INTO purchase_items (purchase_id, product_id, quantity, price_at_purchase)
                    VALUES (?, ?, ?, ?)
                """, (purchase_id, product.product_id, quantity, product.get_final_price()))
            
            conn.commit()
            return purchase_id
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def get_user_purchases(self, user_id):
        """
        Obtiene el historial de compras de un usuario.
        """
        conn = self.db.connect()
        cursor = conn.cursor()
        
        try:
            # Obtener todas las compras del usuario
            cursor.execute("""
                SELECT p.purchase_id, p.purchase_date, p.total_amount,
                       pi.product_id, pi.quantity, pi.price_at_purchase,
                       pr.name
                FROM purchases p
                JOIN purchase_items pi ON p.purchase_id = pi.purchase_id
                JOIN products pr ON pi.product_id = pr.product_id
                WHERE p.user_id = ?
                ORDER BY p.purchase_date DESC
            """, (user_id,))
            
            purchases = {}
            for row in cursor.fetchall():
                purchase_id = row[0]
                if purchase_id not in purchases:
                    purchases[purchase_id] = {
                        'purchase_id': purchase_id,
                        'purchase_date': row[1],
                        'total_amount': row[2],
                        'items': []
                    }
                
                purchases[purchase_id]['items'].append({
                    'product_name': row[6],
                    'quantity': row[4],
                    'price': row[5]
                })
            
            return list(purchases.values())
        finally:
            conn.close()