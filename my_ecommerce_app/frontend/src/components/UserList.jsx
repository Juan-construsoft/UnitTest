import { useState, useEffect } from 'react';
import UserRegistration from './UserRegistration';

function UserList() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showRegistration, setShowRegistration] = useState(false);

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/users');
      if (!response.ok) {
        throw new Error('Error al cargar los usuarios');
      }
      const data = await response.json();
      setUsers(data);
      setLoading(false);
    } catch (error) {
      setError(error.message);
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">Cargando usuarios...</div>;
  }

  if (error) {
    return <div className="error">{error}</div>;
  }

  const handleUserRegistered = () => {
    fetchUsers();
    setShowRegistration(false);
  };

  return (
    <div className="user-list-container">
      <div className="header-actions">
        <h2>Lista de Usuarios</h2>
        <button 
          className="toggle-registration-button"
          onClick={() => setShowRegistration(!showRegistration)}
        >
          {showRegistration ? 'Ocultar Formulario' : 'Nuevo Usuario'}
        </button>
      </div>

      {showRegistration && (
        <UserRegistration onUserRegistered={handleUserRegistered} />
      )}
      {users.length === 0 ? (
        <p>No hay usuarios registrados</p>
      ) : (
        <table className="user-table">
          <thead>
            <tr>
              <th>Nombre de Usuario</th>
              <th>Email</th>
            </tr>
          </thead>
          <tbody>
            {users.map((user) => (
              <tr key={user.user_id}>
                <td>{user.username}</td>
                <td>{user.email}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default UserList;