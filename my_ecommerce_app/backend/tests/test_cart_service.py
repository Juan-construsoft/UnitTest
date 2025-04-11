import unittest
from ..services.cart_service import CartService
from ..services.product_service import ProductService
from ..services.user_service import UserService
from ..models.cart import Cart

class TestCartService(unittest.TestCase):
    def setUp(self):
        self.cart_service = CartService()
        self.user_service = UserService()
        self.product_service = ProductService()
        
        # Create test user and product for cart operations
        self.test_user_id = self.user_service.register_user(
            'test_cart_user',
            'cart_test@example.com',
            'password123'
        )
        
        self.test_product_id = self.product_service.create_product(
            'test_cart_product',
            29.99,
            0,
            100
        )
        
        # Clean up any existing test carts
        self.clean_test_carts()

    def clean_test_carts(self):
        conn = self.cart_service.db.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cart_items WHERE cart_id IN (SELECT cart_id FROM carts WHERE user_id = ?)", (self.test_user_id,))
        cursor.execute("DELETE FROM carts WHERE user_id = ?", (self.test_user_id,))
        conn.commit()
        conn.close()

    def test_create_cart_for_user(self):
        # Test cart creation
        cart_id = self.cart_service.create_cart_for_user(self.test_user_id)
        self.assertIsNotNone(cart_id)

        # Verify cart was created
        cart = self.cart_service.get_cart_by_user_id(self.test_user_id)
        self.assertIsNotNone(cart)
        self.assertEqual(cart.user_id, self.test_user_id)

    def test_get_cart_by_user_id(self):
        # Create a test cart
        cart_id = self.cart_service.create_cart_for_user(self.test_user_id)

        # Test getting existing cart
        cart = self.cart_service.get_cart_by_user_id(self.test_user_id)
        self.assertIsNotNone(cart)
        self.assertEqual(cart.cart_id, cart_id)

        # Test getting non-existent cart
        cart = self.cart_service.get_cart_by_user_id(9999)
        self.assertIsNone(cart)

    def test_add_product_to_cart(self):
        # Create a cart
        cart_id = self.cart_service.create_cart_for_user(self.test_user_id)

        # Test adding product to cart
        self.cart_service.add_product_to_cart(cart_id, self.test_product_id, 2)

        # Verify product was added
        cart_items = self.cart_service.get_cart_items(cart_id)
        self.assertEqual(len(cart_items), 1)
        product, quantity = cart_items[0]
        self.assertEqual(product.product_id, self.test_product_id)
        self.assertEqual(quantity, 2)

        # Test adding more of the same product
        self.cart_service.add_product_to_cart(cart_id, self.test_product_id, 3)
        cart_items = self.cart_service.get_cart_items(cart_id)
        self.assertEqual(len(cart_items), 1)
        product, quantity = cart_items[0]
        self.assertEqual(quantity, 5)  # 2 + 3

    def test_remove_product_from_cart(self):
        # Create a cart and add a product
        cart_id = self.cart_service.create_cart_for_user(self.test_user_id)
        self.cart_service.add_product_to_cart(cart_id, self.test_product_id, 1)

        # Test removing product
        self.cart_service.remove_product_from_cart(cart_id, self.test_product_id)

        # Verify product was removed
        cart_items = self.cart_service.get_cart_items(cart_id)
        self.assertEqual(len(cart_items), 0)

    def test_get_cart_items(self):
        # Create a cart and add products
        cart_id = self.cart_service.create_cart_for_user(self.test_user_id)
        self.cart_service.add_product_to_cart(cart_id, self.test_product_id, 2)

        # Test getting cart items
        cart_items = self.cart_service.get_cart_items(cart_id)
        self.assertEqual(len(cart_items), 1)
        product, quantity = cart_items[0]
        self.assertEqual(product.product_id, self.test_product_id)
        self.assertEqual(quantity, 2)

    def tearDown(self):
        # Clean up test data
        self.clean_test_carts()
        
        # Clean up test user and product
        conn = self.cart_service.db.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE user_id = ?", (self.test_user_id,))
        cursor.execute("DELETE FROM products WHERE product_id = ?", (self.test_product_id,))
        conn.commit()
        conn.close()