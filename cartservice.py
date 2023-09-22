
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

carts = {}

PRODUCT_SERVICE_URL = "https://rest-groceries.onrender.com" 

@app.route('/cart/<int:user_id>', methods=['GET'])
def get_cart(user_id):
    cart = carts.get(user_id, {})
    return jsonify(cart)

@app.route('/cart/<int:user_id>/add/<int:product_id>', methods=['POST'])
def add_to_cart(user_id, product_id):
    data = request.get_json()
    quantity = data.get('quantity', 1)

    product = requests.get(f"{PRODUCT_SERVICE_URL}/products/{product_id}")
    if product.status_code == 404:
        return jsonify({"message": "Product not found"}), 404

    product_data = product.json()
    if 'name' not in product_data or 'price' not in product_data:
        return jsonify({"message": "Invalid product data"}), 500

    product_name = product_data['name']
    product_price = product_data['price']

    cart = carts.setdefault(user_id, {})
    if product_id in cart:
        cart[product_id]['quantity'] += quantity
    else:
        cart[product_id] = {
            'name': product_name,
            'price': product_price,
            'quantity': quantity
        }

    return jsonify({"message": "Product added to cart"}), 200

@app.route('/cart/<int:user_id>/remove/<int:product_id>', methods=['POST'])
def remove_from_cart(user_id, product_id):
    data = request.get_json()
    quantity = data.get('quantity', 1)

    cart = carts.get(user_id, {})
    if product_id in cart:
        cart[product_id]['quantity'] -= quantity
        if cart[product_id]['quantity'] <= 0:
            del cart[product_id]
        return jsonify({"message": "Product removed from cart"}), 200
    else:
        return jsonify({"message": "Product not in cart"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
