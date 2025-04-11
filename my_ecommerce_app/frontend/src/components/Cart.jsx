import { useState, useEffect } from 'react';
import './Cart.css';

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleString();
};

function Cart() {
  const [users, setUsers] = useState([]);
  const [products, setProducts] = useState([]);
  const [selectedUser, setSelectedUser] = useState('');
  const [selectedProduct, setSelectedProduct] = useState('');
  const [quantity, setQuantity] = useState(1);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [message, setMessage] = useState('');
  const [purchases, setPurchases] = useState([]);

  useEffect(() => {
    Promise.all([
      fetch('http://localhost:5000/api/users').then(res => {
        if (!res.ok) throw new Error('Error al cargar usuarios');
        return res.json();
      }),
      fetch('http://localhost:5000/api/products').then(res => {
        if (!res.ok) throw new Error('Error al cargar productos');
        return res.json();
      }),
      fetch('http://localhost:5000/api/purchases')
        .then(res => res.json())
        .then(data => data)
        .catch(() => {
          setPurchases([]);
          return [];
        })
    ])
      .then(([usersData, productsData, purchasesData]) => {
        setUsers(usersData);
        setProducts(productsData);
        setPurchases(purchasesData);
        setLoading(false);
        setError(null);
      })
      .catch(error => {
        setError(error.message || 'Error al cargar los datos');
        setLoading(false);
        setPurchases([]);
      });
  }, []);

  const completePurchase = async () => {
    try {
      const response = await fetch(`http://localhost:5000/api/users/${selectedUser}/purchase`, {
        method: 'POST'
      });

      if (response.ok) {
        setMessage('Compra completada exitosamente');
        // Refresh purchases
        const purchasesRes = await fetch(`http://localhost:5000/api/users/${selectedUser}/purchases`);
        const purchasesData = await purchasesRes.json();
        setPurchases(purchasesData);
      } else {
        throw new Error('Error al completar la compra');
      }
    } catch (error) {
      setMessage('Error al procesar la compra');
    }
  };

  const handlePurchase = async (e) => {
    e.preventDefault();
    if (!selectedUser || !selectedProduct) {
      setMessage('Por favor seleccione un usuario y un producto');
      return;
    }

    try {
      // First create/get cart for user
      const cartResponse = await fetch(`http://localhost:5000/api/users/${selectedUser}/cart`, {
        method: 'POST'
      });
      const cartData = await cartResponse.json();

      // Add product to cart
      const response = await fetch(`http://localhost:5000/api/carts/${cartData.cart_id}/items`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          product_id: selectedProduct,
          quantity: quantity
        })
      });

      if (response.ok) {
        setMessage('Producto agregado al carrito exitosamente');
        setSelectedProduct('');
        setQuantity(1);
      } else {
        throw new Error('Error al agregar al carrito');
      }
    } catch (error) {
      setMessage('Error al procesar la compra');
    }
  };

  if (loading) return <div className="loading">Cargando...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="cart-container">
      {purchases.length > 0 && (
        <div className="purchase-history">
          <h2>Historial de Compras</h2>
          {purchases.map((purchase) => (
            <div key={purchase.purchase_id} className="purchase-item">
              <h3>Compra #{purchase.purchase_id} - {formatDate(purchase.purchase_date)}</h3>
              <p>Total: ${purchase.total_amount}</p>
              <div className="purchase-items">
                {purchase.items.map((item, index) => (
                  <div key={index} className="item">
                    <span>{item.product_name}</span>
                    <span>Cantidad: {item.quantity}</span>
                    <span>Precio: ${item.price}</span>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
      <h2>Realizar Compra</h2>
      <form onSubmit={handlePurchase} className="purchase-form">
        <div className="form-group">
          <label htmlFor="user">Usuario:</label>
          <select
            id="user"
            value={selectedUser}
            onChange={(e) => setSelectedUser(e.target.value)}
            required
          >
            <option value="">Seleccione un usuario</option>
            {users.map(user => (
              <option key={user.user_id} value={user.user_id}>
                {user.username}
              </option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="product">Producto:</label>
          <select
            id="product"
            value={selectedProduct}
            onChange={(e) => setSelectedProduct(e.target.value)}
            required
          >
            <option value="">Seleccione un producto</option>
            {products.map(product => (
              <option key={product.product_id} value={product.product_id}>
                {product.name} - ${product.price}
              </option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="quantity">Cantidad:</label>
          <input
            type="number"
            id="quantity"
            min="1"
            value={quantity}
            onChange={(e) => setQuantity(parseInt(e.target.value))}
            required
          />
        </div>

        <button type="submit" className="purchase-button">
          Agregar al Carrito
        </button>
      </form>
      
      {selectedUser && (
        <button onClick={completePurchase} className="complete-purchase-button">
          Completar Compra
        </button>
      )}

      {message && <div className="message">{message}</div>}
    </div>
  );
}

export default Cart;