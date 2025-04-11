# backend/models/cart.py

__all__ = ['Cart']

class Cart:
    """
    Representa un carrito asociado a un user_id.
    """
    def __init__(self, cart_id, user_id):
        self.cart_id = cart_id
        self.user_id = user_id

    def __repr__(self):
        return f"<Cart {self.cart_id} de User {self.user_id}>"
