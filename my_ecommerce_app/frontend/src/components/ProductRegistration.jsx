import { useState } from 'react';
import './ProductRegistration.css';

function ProductRegistration({ onProductRegistered }) {
  const [formData, setFormData] = useState({
    name: '',
    price: '',
    stock: '',
    description: ''
  });

  const [errors, setErrors] = useState({});
  const [successMessage, setSuccessMessage] = useState('');

  const validateForm = () => {
    const newErrors = {};
    if (!formData.name.trim()) {
      newErrors.name = 'El nombre del producto es requerido';
    }
    if (!formData.price.trim()) {
      newErrors.price = 'El precio es requerido';
    } else if (isNaN(formData.price) || Number(formData.price) <= 0) {
      newErrors.price = 'El precio debe ser un número válido mayor que 0';
    }
    if (!formData.stock.trim()) {
      newErrors.stock = 'La cantidad en stock es requerida';
    } else if (isNaN(formData.stock) || !Number.isInteger(Number(formData.stock)) || Number(formData.stock) < 0) {
      newErrors.stock = 'La cantidad en stock debe ser un número entero no negativo';
    }
    if (!formData.description.trim()) {
      newErrors.description = 'La descripción es requerida';
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
        const response = await fetch('http://localhost:5000/api/products/register', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(formData),
        });

        if (response.ok) {
          setSuccessMessage('Producto registrado exitosamente!');
          setFormData({ name: '', price: '', stock: '', description: '' });
          if (onProductRegistered) {
            onProductRegistered();
          }
        } else {
          const data = await response.json();
          setErrors({ submit: data.message || 'Error al registrar producto' });
        }
      } catch (error) {
        setErrors({ submit: 'Error de conexión' });
      }
    }
  };

  return (
    <div className="registration-container">
      <h2>Registro de Producto</h2>
      {successMessage && (
        <div className="success-message">{successMessage}</div>
      )}
      {errors.submit && (
        <div className="error-message">{errors.submit}</div>
      )}
      <form onSubmit={handleSubmit} className="registration-form">
        <div className="form-group">
          <label htmlFor="name">Nombre del Producto:</label>
          <input
            type="text"
            id="name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            className={errors.name ? 'error' : ''}
          />
          {errors.name && (
            <span className="error-text">{errors.name}</span>
          )}
        </div>

        <div className="form-group">
          <label htmlFor="price">Precio:</label>
          <input
            type="number"
            id="price"
            name="price"
            value={formData.price}
            onChange={handleChange}
            step="0.01"
            min="0"
            className={errors.price ? 'error' : ''}
          />
          {errors.price && (
            <span className="error-text">{errors.price}</span>
          )}
        </div>

        <div className="form-group">
          <label htmlFor="stock">Cantidad en Stock:</label>
          <input
            type="number"
            id="stock"
            name="stock"
            value={formData.stock}
            onChange={handleChange}
            min="0"
            step="1"
            className={errors.stock ? 'error' : ''}
          />
          {errors.stock && (
            <span className="error-text">{errors.stock}</span>
          )}
        </div>

        <div className="form-group">
          <label htmlFor="description">Descripción:</label>
          <textarea
            id="description"
            name="description"
            value={formData.description}
            onChange={handleChange}
            className={errors.description ? 'error' : ''}
          />
          {errors.description && (
            <span className="error-text">{errors.description}</span>
          )}
        </div>

        <button type="submit" className="submit-button">
          Registrar Producto
        </button>
      </form>
    </div>
  );
}

export default ProductRegistration;