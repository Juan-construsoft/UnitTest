# cliente.py

import re

class Cliente:
    def __init__(self, id, nombre, apellido, correo, edad, activo):
        """
        Constructor de la clase Cliente.
        Valida los datos antes de crear el objeto.
        """
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.correo = correo
        self.edad = edad
        self.activo = activo

        # Validaciones
        self.validar_id(id)
        self.validar_nombre_apellido(nombre, "nombre")
        self.validar_nombre_apellido(apellido, "apellido")
        self.validar_correo(correo)
        self.validar_edad(edad)
        self.validar_activo(activo)

    @staticmethod
    def validar_id(id):
        if not isinstance(id, int) or id <= 0:
            raise ValueError("El ID debe ser un número entero positivo.")

    @staticmethod
    def validar_nombre_apellido(valor, campo):
        if not valor or not isinstance(valor, str) or valor.strip() == "":
            raise ValueError(f"El {campo} no puede estar vacío ni ser nulo.")

    @staticmethod
    def validar_correo(correo):
        patron = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(patron, correo):
            raise ValueError("El correo electrónico no tiene un formato válido.")

    @staticmethod
    def validar_edad(edad):
        if not isinstance(edad, int) or edad < 18 or edad >= 100:
            raise ValueError("La edad debe ser un número entero entre 18 y 99 años.")

    @staticmethod
    def validar_activo(activo):
        if activo not in ["si", "no"]:
            raise ValueError("El campo 'activo' debe ser 'si' o 'no'.")

    def __repr__(self):
        return f"Cliente(id={self.id}, nombre={self.nombre}, apellido={self.apellido}, correo={self.correo}, edad={self.edad}, activo={self.activo})"


class ClienteDB:
    def __init__(self):
        """
        Inicializa una base de datos simulada como un diccionario.
        """
        self.clientes = {}

    def agregar_cliente(self, cliente):
        """
        Agrega un cliente a la base de datos si su ID no está duplicado.
        """
        if cliente.id in self.clientes:
            raise ValueError(f"Ya existe un cliente con el ID {cliente.id}.")
        self.clientes[cliente.id] = cliente

    def obtener_cliente_por_id(self, cliente_id):
        """
        Recupera un cliente por su ID.
        """
        return self.clientes.get(cliente_id, None)

    def actualizar_cliente(self, cliente_id, **kwargs):
        """
        Actualiza los datos de un cliente existente.
        """
        if cliente_id not in self.clientes:
            raise ValueError(f"No existe un cliente con el ID {cliente_id}.")

        cliente = self.clientes[cliente_id]
        for key, value in kwargs.items():
            if hasattr(cliente, key):
                setattr(cliente, key, value)
            else:
                raise ValueError(f"El campo '{key}' no es válido para un cliente.")

    def eliminar_cliente(self, cliente_id):
        """
        Elimina un cliente por su ID.
        """
        if cliente_id not in self.clientes:
            raise ValueError(f"No existe un cliente con el ID {cliente_id}.")
        del self.clientes[cliente_id]

    def listar_clientes(self):
        """
        Devuelve una lista de todos los clientes en la base de datos.
        """
        return list(self.clientes.values())