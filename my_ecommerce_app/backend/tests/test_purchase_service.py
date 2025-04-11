import unittest
from ..services.purchase_service import PurchaseService
from ..services.cart_service import CartService
from ..services.product_service import ProductService
from ..services.user_service import UserService

class TestPurchaseService(unittest.TestCase):
    def setUp(self):
        self.purchase_service = PurchaseService()
        self.cart_service = CartService()
        self.user_service = UserService()
        self.product_service = ProductService()
        
        # Create test user and product
        self.test_user_id = self.user_service.register_user(
            'test_purchase_user',
            'purchase_test@example.com',
            'password123'
        )
        
        self.test_product_id = self.product_service.create_product(
            'test_purchase_product',
            29.99,
            0,
            100
        )
        
        # Create cart and add product
        self.cart_id = self.cart_service.create_cart_for_user(self.test_user_id)
        self.cart_service.add_product_to_cart(self.cart_id, self.test_product_id, 2)
        
        # Clean up any existing test purchases
        self.clean_test_purchases()
    
    def clean_test_purchases(self):
        conn = self.purchase_service.db.connect()
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM purchase_items 
            WHERE purchase_id IN (
                SELECT purchase_id FROM purchases 
                WHERE user_id = ?
            )
        """, (self.test_user_id,))
        cursor.execute("DELETE FROM purchases WHERE user_id = ?", (self.test_user_id,))
        conn.commit()
        conn.close()
    
    def test_create_purchase(self):
        # Get cart items for purchase
        cart_items = self.cart_service.get_cart_items(self.cart_id)
        total_amount = sum(product.get_final_price() * quantity for product, quantity in cart_items)
        
        # Test purchase creation
        purchase_id = self.purchase_service.create_purchase(
            self.test_user_id,
            cart_items,
            total_amount
        )
        self.assertIsNotNone(purchase_id)
        
        # Verify purchase was created
        purchases = self.purchase_service.get_user_purchases(self.test_user_id)
        self.assertEqual(len(purchases), 1)
        purchase = purchases[0]
        self.assertEqual(purchase['purchase_id'], purchase_id)
        self.assertEqual(len(purchase['items']), 1)
        self.assertEqual(purchase['total_amount'], total_amount)
    
    def test_get_user_purchases(self):
        # Create multiple purchases
        cart_items = self.cart_service.get_cart_items(self.cart_id)
        total_amount = sum(product.get_final_price() * quantity for product, quantity in cart_items)
        
        purchase_ids = []
        for _ in range(2):
            purchase_id = self.purchase_service.create_purchase(
                self.test_user_id,
                cart_items,
                total_amount
            )
            purchase_ids.append(purchase_id)
        
        # Test getting purchase history
        purchases = self.purchase_service.get_user_purchases(self.test_user_id)
        self.assertEqual(len(purchases), 2)
        
        # Verify purchase details
        for purchase in purchases:
            self.assertIn(purchase['purchase_id'], purchase_ids)
            self.assertEqual(purchase['total_amount'], total_amount)
            self.assertEqual(len(purchase['items']), 1)
            item = purchase['items'][0]
            self.assertEqual(item['product_name'], 'test_purchase_product')
            self.assertEqual(item['quantity'], 2)
    
    def test_get_user_purchases_empty(self):
        # Test getting purchases for user with no history
        purchases = self.purchase_service.get_user_purchases(9999)
        self.assertEqual(len(purchases), 0)
    
    def tearDown(self):
        # Clean up test data
        self.clean_test_purchases()
        
        # Clean up cart data
        conn = self.cart_service.db.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cart_items WHERE cart_id = ?", (self.cart_id,))
        cursor.execute("DELETE FROM carts WHERE user_id = ?", (self.test_user_id,))
        
        # Clean up user and product
        cursor.execute("DELETE FROM users WHERE user_id = ?", (self.test_user_id,))
        cursor.execute("DELETE FROM products WHERE product_id = ?", (self.test_product_id,))
        conn.commit()
        conn.close()