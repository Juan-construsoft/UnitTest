import { Link } from 'react-router-dom';
import './NavBar.css';
import { FaUserPlus, FaBox, FaShoppingCart, FaHome } from 'react-icons/fa';

function NavBar() {
  return (
    <nav className="navbar">
      <Link to="/" className="nav-item">
        <FaHome className="nav-icon" />
        <span>Inicio</span>
      </Link>
      <Link to="/users" className="nav-item">
        <FaUserPlus className="nav-icon" />
        <span>Usuarios</span>
      </Link>
      <Link to="/products" className="nav-item">
        <FaBox className="nav-icon" />
        <span>Productos</span>
      </Link>
      <Link to="/cart" className="nav-item">
        <FaShoppingCart className="nav-icon" />
        <span>Compras</span>
      </Link>
    </nav>
  );
}

export default NavBar;