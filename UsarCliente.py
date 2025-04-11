# Importar las clases necesarias
from cliente import Cliente, ClienteDB

# Crear una instancia de la base de datos
db = ClienteDB()

try:
    # Crear clientes válidos
    cliente1 = Cliente(1, "Juan", "Pérez", "juan@example.com", 25, "si")
    cliente2 = Cliente(2, "María", "López", "maria@example.com", 30, "no")

    print("\n=== Agregando clientes ===")
    # Agregar clientes a la base de datos
    db.agregar_cliente(cliente1)
    db.agregar_cliente(cliente2)

    print("\n=== Listando todos los clientes ===")
    print(db.listar_clientes())

    print("\n=== Obteniendo cliente por ID ===")
    cliente = db.obtener_cliente_por_id(1)
    print(cliente)

    print("\n=== Actualizando cliente ===")
    db.actualizar_cliente(1, correo="nuevo.juan@example.com", activo="no")
    print("Cliente actualizado:")
    print(db.obtener_cliente_por_id(1))

    print("\n=== Eliminando cliente ===")
    db.eliminar_cliente(2)
    print("Clientes restantes:")
    print(db.listar_clientes())

except ValueError as e:
    print(f"Error: {e}")
except Exception as e:
    print(f"Error inesperado: {e}")