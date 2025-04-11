# frontend/main.py

from backend.services.user_service import UserService
from backend.services.product_service import ProductService
from backend.services.cart_service import CartService

def main():
    user_service = UserService()
    product_service = ProductService()
    cart_service = CartService()

    while True:
        print("\n--- Menú Principal ---")
        print("1. Registrar usuario")
        print("2. Iniciar sesión")
        print("3. Crear producto (admin)")
        print("4. Salir")
        choice = input("Elige una opción: ")

        if choice == "1":
            username = input("Nombre de usuario: ")
            email = input("Email: ")
            password = input("Contraseña: ")
            user_id = user_service.register_user(username, email, password)
            print(f"Usuario creado con ID = {user_id}")

        elif choice == "2":
            username = input("Nombre de usuario: ")
            password = input("Contraseña: ")
            if user_service.login(username, password):
                print("Login exitoso.")
                user = user_service.get_user_by_username(username)
                user_menu(user, cart_service, product_service)
            else:
                print("Credenciales inválidas.")

        elif choice == "3":
            # Creación manual de un producto
            name = input("Nombre del producto: ")
            price = float(input("Precio: "))
            discount = float(input("Descuento (0 a 1): "))
            stock = int(input("Stock inicial: "))
            pid = product_service.create_product(name, price, discount, stock)
            print(f"Producto creado con ID = {pid}")

        elif choice == "4":
            print("Saliendo...")
            break

        else:
            print("Opción inválida.")

def user_menu(user, cart_service, product_service):
    while True:
        print(f"\n--- Menú Usuario ({user.username}) ---")
        print("1. Crear/Obtener mi carrito")
        print("2. Agregar producto al carrito")
        print("3. Ver total del carrito")
        print("4. Regresar al menú principal")
        choice = input("Elige una opción: ")

        if choice == "1":
            cart = cart_service.get_cart_by_user_id(user.user_id)
            if cart:
                print(f"Ya tienes un carrito con ID {cart.cart_id}")
            else:
                new_cart_id = cart_service.create_cart_for_user(user.user_id)
                print(f"Carrito creado con ID {new_cart_id}")

        elif choice == "2":
            cart = cart_service.get_cart_by_user_id(user.user_id)
            if not cart:
                print("No tienes un carrito. Créalo primero.")
                continue
            product_id = input("ID del producto: ")
            quantity = int(input("Cantidad: "))
            cart_service.add_product_to_cart(cart.cart_id, product_id, quantity)
            print("Producto(s) agregados al carrito.")

        elif choice == "3":
            cart = cart_service.get_cart_by_user_id(user.user_id)
            if not cart:
                print("No tienes un carrito.")
                continue
            total = cart_service.get_cart_total(cart.cart_id)
            print(f"El total de tu carrito es: {total:.2f}")

        elif choice == "4":
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    main()
