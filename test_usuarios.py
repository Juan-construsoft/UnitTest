import unittest
from unittest.mock import Mock
from Usuarios import UsuarioRepository

class TestUsuarioRepository(unittest.TestCase):
    def setUp(self):
        self.mock_db = Mock()
        self.usuario_repository = UsuarioRepository(self.mock_db)

    def test_crear_usuario(self):
        # Arrange
        usuario_test = {"id": 1, "nombre": "Test User"}
        
        # Act
        self.usuario_repository.crear_usuario(usuario_test)
        
        # Assert
        self.mock_db.insertar_usuario.assert_called_once_with(usuario_test)

    def test_obtener_usuario_por_id(self):
        # Arrange
        usuario_id = 1
        usuario_esperado = {"id": 1, "nombre": "Test User"}
        self.mock_db.obtener_usuario.return_value = usuario_esperado
        
        # Act
        resultado = self.usuario_repository.obtener_usuario_por_id(usuario_id)
        
        # Assert
        self.mock_db.obtener_usuario.assert_called_once_with(usuario_id)
        self.assertEqual(resultado, usuario_esperado)

    def test_actualizar_usuario(self):
        # Arrange
        usuario_id = 1
        datos_actualizacion = {"nombre": "Updated User"}
        
        # Act
        self.usuario_repository.actualizar_usuario(usuario_id, datos_actualizacion)
        
        # Assert
        self.mock_db.actualizar_usuario.assert_called_once_with(usuario_id, datos_actualizacion)

    def test_eliminar_usuario(self):
        # Arrange
        usuario_id = 1
        
        # Act
        self.usuario_repository.eliminar_usuario(usuario_id)
        
        # Assert
        self.mock_db.eliminar_usuario.assert_called_once_with(usuario_id)

if __name__ == '__main__':
    unittest.main()