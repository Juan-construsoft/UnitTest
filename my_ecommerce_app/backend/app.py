from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from services.user_service import UserService
from services.product_service import ProductService
from services.cart_service import CartService
from services.purchase_service import PurchaseService

app = Flask(__name__, static_folder='../frontend/dist', template_folder='../frontend/dist', static_url_path='')
CORS(app)

user_service = UserService()
product_service = ProductService()
cart_service = CartService()
purchase_service = PurchaseService()

@app.route('/')
@app.route('/<path:path>')
def index(path=''):
    return render_template('index.html')

@app.route('/api/users/register', methods=['POST'])
def register():
    data = request.get_json()
    try:
        user_id = user_service.register_user(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )
        return jsonify({'message': 'Usuario registrado exitosamente', 'user_id': user_id}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 400

@app.route('/api/products/register', methods=['POST'])
def register_product():
    data = request.get_json()
    try:
        product_id = product_service.create_product(
            name=data['name'],
            price=float(data['price']),
            discount=0.0,  # Default value for now
            stock=int(data['stock'])
        )
        return jsonify({'message': 'Producto registrado exitosamente', 'product_id': product_id}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 400

@app.route('/api/users', methods=['GET'])
def get_users():
    try:
        users = user_service.get_all_users()
        return jsonify([{
            'user_id': u.user_id,
            'username': u.username,
            'email': u.email
        } for u in users]), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route('/api/products', methods=['GET'])
def get_products():
    try:
        products = product_service.get_all_products()
        return jsonify([{
            'product_id': p.product_id,
            'name': p.name,
            'price': p.price,
            'stock': p.stock,
            'discount': p.discount
        } for p in products]), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route('/api/users/<int:user_id>/cart', methods=['POST'])
def create_or_get_cart(user_id):
    try:
        cart = cart_service.get_cart_by_user_id(user_id)
        if not cart:
            cart_id = cart_service.create_cart_for_user(user_id)
            return jsonify({'cart_id': cart_id}), 201
        return jsonify({'cart_id': cart.cart_id}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route('/api/carts/<int:cart_id>/items', methods=['POST'])
def add_to_cart(cart_id):
    data = request.get_json()
    try:
        cart_service.add_product_to_cart(
            cart_id=cart_id,
            product_id=int(data['product_id']),
            quantity=int(data['quantity'])
        )
        return jsonify({'message': 'Producto agregado al carrito exitosamente'}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 400

@app.route('/api/users/<int:user_id>/purchases', methods=['GET'])
def get_user_purchases(user_id):
    try:
        purchases = purchase_service.get_user_purchases(user_id)
        return jsonify(purchases), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route('/api/users/<int:user_id>/purchase', methods=['POST'])
def create_purchase(user_id):
    try:
        cart = cart_service.get_cart_by_user_id(user_id)
        if not cart:
            return jsonify({'message': 'No cart found for user'}), 404
            
        cart_items = cart_service.get_cart_items(cart.cart_id)
        if not cart_items:
            return jsonify({'message': 'Cart is empty'}), 400
            
        total = cart_service.get_cart_total(cart.cart_id)
        purchase_id = purchase_service.create_purchase(user_id, cart_items, total)
        
        return jsonify({
            'message': 'Purchase completed successfully',
            'purchase_id': purchase_id
        }), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)