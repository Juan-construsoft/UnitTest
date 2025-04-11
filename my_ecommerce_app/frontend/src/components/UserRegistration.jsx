import { useState } from 'react';
import './UserRegistration.css';

function UserRegistration({ onUserRegistered }) {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: ''
  });

  const [errors, setErrors] = useState({});
  const [successMessage, setSuccessMessage] = useState('');

  const validateForm = () => {
    const newErrors = {};
    if (!formData.username.trim()) {
      newErrors.username = 'El nombre de usuario es requerido';
    }
    if (!formData.email.trim()) {
      newErrors.email = 'El email es requerido';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'El email no es válido';
    }
    if (!formData.password.trim()) {
      newErrors.password = 'La contraseña es requerida';
    } else if (formData.password.length < 6) {
      newErrors.password = 'La contraseña debe tener al menos 6 caracteres';
    }
    return newErrors;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prevData => ({
      ...prevData,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const newErrors = validateForm();
    setErrors(newErrors);

    if (Object.keys(newErrors).length === 0) {
      try {
        const response = await fetch('http://localhost:5000/api/users/register', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(formData),
        });

        if (response.ok) {
          setSuccessMessage('Usuario registrado exitosamente!');
          setFormData({ username: '', email: '', password: '' });
          if (onUserRegistered) {
            onUserRegistered();
          }
        } else {
          const data = await response.json();
          setErrors({ submit: data.message || 'Error al registrar usuario' });
        }
      } catch (error) {
        setErrors({ submit: 'Error de conexión' });
      }
    }
  };

  return (
    <div className="registration-container">
      <h2>Registro de Usuario</h2>
      {successMessage && (
        <div className="success-message">{successMessage}</div>
      )}
      {errors.submit && (
        <div className="error-message">{errors.submit}</div>
      )}
      <form onSubmit={handleSubmit} className="registration-form">
        <div className="form-group">
          <label htmlFor="username">Nombre de Usuario:</label>
          <input
            type="text"
            id="username"
            name="username"
            value={formData.username}
            onChange={handleChange}
            className={errors.username ? 'error' : ''}
          />
          {errors.username && (
            <span className="error-text">{errors.username}</span>
          )}
        </div>

        <div className="form-group">
          <label htmlFor="email">Email:</label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            className={errors.email ? 'error' : ''}
          />
          {errors.email && (
            <span className="error-text">{errors.email}</span>
          )}
        </div>

        <div className="form-group">
          <label htmlFor="password">Contraseña:</label>
          <input
            type="password"
            id="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            className={errors.password ? 'error' : ''}
          />
          {errors.password && (
            <span className="error-text">{errors.password}</span>
          )}
        </div>

        <button type="submit" className="submit-button">
          Registrarse
        </button>
      </form>
    </div>
  );
}

export default UserRegistration;