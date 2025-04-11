import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import './App.css'
import Dashboard from './components/Dashboard'
import UserRegistration from './components/UserRegistration'
import ProductRegistration from './components/ProductRegistration'
import ProductList from './components/ProductList'
import UserList from './components/UserList'
import Cart from './components/Cart'
import NavBar from './components/NavBar'

function App() {
  return (
    <Router>
      <div className="app-container">
        <header className="app-header">
          <h1>Mi E-commerce</h1>
          <NavBar />
        </header>
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/users" element={<UserList />} />
            <Route path="/products/register" element={<ProductRegistration />} />
            <Route path="/products" element={<ProductList />} />
            <Route path="/cart" element={<Cart />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App