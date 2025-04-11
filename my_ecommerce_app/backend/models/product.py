# backend/models/product.py

class Product:
    def __init__(self, product_id, name, price, discount=0.0, stock=0):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.discount = discount  # % de descuento, e.g. 0.1 = 10% descuento
        self.stock = stock

    def get_final_price(self):
        """
        Retorna el precio final del producto aplicando el descuento.
        """
        return self.price * (1 - self.discount)

    def __repr__(self):
        return f"<Product {self.product_id}: {self.name} (${self.price}, -{self.discount*100}% )>"
