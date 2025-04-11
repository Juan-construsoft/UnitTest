class UsuarioRepository:
    def __init__(self, db):
        self.db = db

    def crear_usuario(self, usuario):
        self.db.insertar_usuario(usuario)

    def obtener_usuario_por_id(self, usuario_id):
        return self.db.obtener_usuario(usuario_id)

    def actualizar_usuario(self, usuario_id, datos):
        self.db.actualizar_usuario(usuario_id, datos)

    def eliminar_usuario(self, usuario_id):
        self.db.eliminar_usuario(usuario_id)
