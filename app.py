from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all origins, adjust as needed

# MySQL database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'cafe_management'
}

@app.route('/submit_order', methods=['POST'])
def submit_order():
    data = request.json
    orders = data.get('orders', [])
    total = data.get('total', 0)
    phone_number = data.get('phone_number')  # Retrieve the phone number

    if not phone_number:
        return jsonify({"status": "error", "message": "Phone number is required"}), 400

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        for order in orders:
            query = """
                INSERT INTO orderstable (phone_number, coffee_name, size, quantity, price, total)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                phone_number, 
                order['name'], 
                order['size'], 
                order['quantity'], 
                order['price'], 
                order['total']
            ))

        conn.commit()
        return jsonify({"status": "success", "message": "Order submitted successfully!"})
    except mysql.connector.Error as err:
        conn.rollback()
        return jsonify({"status": "error", "message": f"Database error: {err}"}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/get_orders', methods=['GET'])
def get_orders():
    phone_number = request.args.get('phone_number')  # Retrieve phone number from query params

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        if phone_number:
            # Fetch orders for the specific phone number
            query = "SELECT * FROM orderstable WHERE phone_number = %s"
            cursor.execute(query, (phone_number,))
        else:
            # Fetch all orders if no phone number is provided
            query = "SELECT * FROM orderstable"
            cursor.execute(query)

        orders = cursor.fetchall()

        # Calculate total income
        total_income = sum(order['total'] for order in orders)

        return jsonify({
            "status": "success",
            "orders": orders,
            "total_income": total_income  # Return total income along with the orders
        })
    except mysql.connector.Error as err:
        return jsonify({"status": "error", "message": f"Database error: {err}"}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
