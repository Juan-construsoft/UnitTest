class Proveedor:
    """Representa a un proveedor."""

    def __init__(self, identificacion, nombre, direccion, representante, correo, telefono):
        self.identificacion = identificacion
        self.nombre = nombre
        self.direccion = direccion
        self.representante = representante
        self.correo = correo
        self.telefono = telefono

        self.validar_identificacion(identificacion)
        self.validar_campo_texto(nombre, "nombre")
        self.validar_campo_texto(direccion, "direccion")
        self.validar_campo_texto(representante, "representante")
        self.validar_correo(correo)
        self.validar_campo_texto(telefono, "telefono")

    @staticmethod
    def validar_identificacion(identificacion):
        if not isinstance(identificacion, int) or identificacion <= 0:
            raise ValueError("La identificacion debe ser un numero entero positivo.")

    @staticmethod
    def validar_campo_texto(valor, campo):
        if not valor or not isinstance(valor, str) or valor.strip() == "":
            raise ValueError(f"El campo '{campo}' no puede estar vacio.")

    @staticmethod
    def validar_correo(correo):
        import re
        patron = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(patron, correo):
            raise ValueError("El correo electronico no tiene un formato valido.")


class ProveedorDB:
    """Base de datos simulada para proveedores."""

    def __init__(self):
        self.proveedores = {}

    def agregar_proveedor(self, proveedor):
        if proveedor.identificacion in self.proveedores:
            raise ValueError(f"Ya existe un proveedor con el ID {proveedor.identificacion}.")
        self.proveedores[proveedor.identificacion] = proveedor

    def obtener_proveedor_por_id(self, proveedor_id):
        return self.proveedores.get(proveedor_id, None)

    def actualizar_proveedor(self, proveedor_id, **kwargs):
        if proveedor_id not in self.proveedores:
            raise ValueError(f"No existe un proveedor con el ID {proveedor_id}.")
        proveedor = self.proveedores[proveedor_id]
        for key, value in kwargs.items():
            if hasattr(proveedor, key):
                setattr(proveedor, key, value)
            else:
                raise ValueError(f"El campo '{key}' no es valido para un proveedor.")

    def eliminar_proveedor(self, proveedor_id):
        if proveedor_id not in self.proveedores:
            raise ValueError(f"No existe un proveedor con el ID {proveedor_id}.")
        del self.proveedores[proveedor_id]

