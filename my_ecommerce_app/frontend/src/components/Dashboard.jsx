import React from 'react';
import { Link } from 'react-router-dom';
import './Dashboard.css';
import { FaUserPlus, FaBox, FaShoppingCart } from 'react-icons/fa';

const Dashboard = () => {
  return (
    <div className="dashboard-container">
      <h2 className="dashboard-title">Panel de Control</h2>
      <div className="dashboard-grid">
        <Link to="/users" className="dashboard-card">
          <FaUserPlus className="dashboard-icon" />
          <h3>Gestión de Usuarios</h3>
          <p>Ver y registrar usuarios</p>
        </Link>
        <Link to="/products" className="dashboard-card">
          <FaBox className="dashboard-icon" />
          <h3>Gestión de Productos</h3>
          <p>Agregar y administrar productos</p>
        </Link>
        <Link to="/cart" className="dashboard-card">
          <FaShoppingCart className="dashboard-icon" />
          <h3>Realizar Compra</h3>
          <p>Explorar y comprar productos</p>
        </Link>
      </div>
    </div>
  );
};

export default Dashboard;