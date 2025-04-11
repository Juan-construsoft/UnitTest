import unittest
from ..services.product_service import ProductService
from ..models.product import Product

class TestProductService(unittest.TestCase):
    def setUp(self):
        self.product_service = ProductService()
        # Clean up any test products from previous runs
        self.clean_test_products()

    def clean_test_products(self):
        conn = self.product_service.db.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products WHERE name LIKE 'test_product%'")
        conn.commit()
        conn.close()

    def test_create_product(self):
        # Test product creation
        product_id = self.product_service.create_product(
            'test_product1',
            99.99,
            10,  # 10% discount
            50   # initial stock
        )
        self.assertIsNotNone(product_id)

        # Verify product was created
        product = self.product_service.get_product_by_id(product_id)
        self.assertIsNotNone(product)
        self.assertEqual(product.name, 'test_product1')
        self.assertEqual(product.price, 99.99)
        self.assertEqual(product.discount, 10)
        self.assertEqual(product.stock, 50)

    def test_get_product_by_id(self):
        # Create a test product
        product_id = self.product_service.create_product(
            'test_product2',
            49.99,
            0,
            100
        )

        # Test getting existing product
        product = self.product_service.get_product_by_id(product_id)
        self.assertIsNotNone(product)
        self.assertEqual(product.name, 'test_product2')
        self.assertEqual(product.price, 49.99)

        # Test getting non-existent product
        product = self.product_service.get_product_by_id(9999)
        self.assertIsNone(product)

    def test_update_product_stock(self):
        # Create a test product
        product_id = self.product_service.create_product(
            'test_product3',
            29.99,
            5,
            75
        )

        # Test updating stock
        result = self.product_service.update_product_stock(product_id, 60)
        self.assertEqual(result, 1)  # 1 row affected

        # Verify stock was updated
        product = self.product_service.get_product_by_id(product_id)
        self.assertEqual(product.stock, 60)

        # Test updating non-existent product
        result = self.product_service.update_product_stock(9999, 50)
        self.assertEqual(result, 0)  # 0 rows affected

    def test_delete_product(self):
        # Create a test product
        product_id = self.product_service.create_product(
            'test_product4',
            19.99,
            0,
            25
        )

        # Test deleting existing product
        result = self.product_service.delete_product(product_id)
        self.assertEqual(result, 1)  # 1 row affected

        # Verify product was deleted
        product = self.product_service.get_product_by_id(product_id)
        self.assertIsNone(product)

        # Test deleting non-existent product
        result = self.product_service.delete_product(9999)
        self.assertEqual(result, 0)  # 0 rows affected

    def test_get_all_products(self):
        # Create multiple test products
        test_products = [
            ('test_product5', 39.99, 0, 30),
            ('test_product6', 59.99, 15, 40)
        ]
        for name, price, discount, stock in test_products:
            self.product_service.create_product(name, price, discount, stock)

        # Test getting all products
        products = self.product_service.get_all_products()
        self.assertIsNotNone(products)
        self.assertIsInstance(products, list)
        
        # Verify test products are in the list
        test_names = [product[0] for product in test_products]
        found_products = [product for product in products if product.name in test_names]
        self.assertEqual(len(found_products), len(test_products))

    def tearDown(self):
        # Clean up test products
        self.clean_test_products()