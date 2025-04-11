import { useState, useEffect } from 'react';
import './ProductList.css';
import ProductRegistration from './ProductRegistration';

function ProductList() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showRegistration, setShowRegistration] = useState(false);

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/products');
      if (!response.ok) {
        throw new Error('Error al cargar los productos');
      }
      const data = await response.json();
      setProducts(data);
      setLoading(false);
    } catch (error) {
      setError(error.message);
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">Cargando productos...</div>;
  }

  if (error) {
    return <div className="error">{error}</div>;
  }

  const handleProductRegistered = () => {
    fetchProducts();
    setShowRegistration(false);
  };

  return (
    <div className="product-list-container">
      <div className="header-actions">
        <h2>Lista de Productos</h2>
        <button 
          className="toggle-registration-button"
          onClick={() => setShowRegistration(!showRegistration)}
        >
          {showRegistration ? 'Ocultar Formulario' : 'Nuevo Producto'}
        </button>
      </div>

      {showRegistration && (
        <ProductRegistration onProductRegistered={handleProductRegistered} />
      )}
      {products.length === 0 ? (
        <p>No hay productos registrados</p>
      ) : (
        <table className="product-table">
          <thead>
            <tr>
              <th>Nombre</th>
              <th>Precio</th>
              <th>Stock</th>
              <th>Descripción</th>
            </tr>
          </thead>
          <tbody>
            {products.map((product) => (
              <tr key={product.product_id}>
                <td>{product.name}</td>
                <td>${product.price}</td>
                <td>{product.stock}</td>
                <td>{product.description}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default ProductList;