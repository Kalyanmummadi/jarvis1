from flask import Flask, render_template, request, jsonify
import mysql.connector 

app = Flask(__name__)

# Database connection
db = mysql.connector.connect(
    host="http://127.0.0.1:5000",
    user="kalyanmummadi830@gmail.com",
    password="K@ly@n830",
    database="grocery_store"
)
cursor = db.cursor(dictionary=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/products')
def products():
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    return render_template('products.html', products=products)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = request.json['product_id']
    quantity = request.json['quantity']
    
    cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
    product = cursor.fetchone()
    
    if product:
        total_price = product['price'] * quantity
        cursor.execute("INSERT INTO cart (product_id, quantity, total_price) VALUES (%s, %s, %s)",
                       (product_id, quantity, total_price))
        db.commit()
        return jsonify({"success": True, "message": "Product added to cart"})
    else:
        return jsonify({"success": False, "message": "Product not found"})

@app.route('/cart')
def cart():
    cursor.execute("SELECT c.id, p.name, c.quantity, c.total_price FROM cart c JOIN products p ON c.product_id = p.id")
    cart_items = cursor.fetchall()
    return render_template('cart.html', cart_items=cart_items)

if __name__ == '__main__':
    app.run(debug=True)