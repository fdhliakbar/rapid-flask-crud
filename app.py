# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import json

app = Flask(__name__)
CORS(app)

# Initialize database
def init_db():
    conn = sqlite3.connect('customers.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT
        )
    ''')
    conn.close()

# GET - Read all customers
@app.route('/customers', methods=['GET'])
def get_customers():
    conn = sqlite3.connect('customers.db')
    conn.row_factory = sqlite3.Row
    customers = conn.execute('SELECT * FROM customers').fetchall()
    conn.close()
    return jsonify([dict(row) for row in customers])

# POST - Create customer
@app.route('/customers', methods=['POST'])
def create_customer():
    data = request.json
    conn = sqlite3.connect('customers.db')
    conn.execute('INSERT INTO customers (name, email, phone) VALUES (?, ?, ?)',
                 (data['name'], data['email'], data.get('phone', '')))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Customer created successfully'}), 201

# PUT - Update customer
@app.route('/customers/<int:id>', methods=['PUT'])
def update_customer(id):
    data = request.json
    conn = sqlite3.connect('customers.db')
    conn.execute('UPDATE customers SET name=?, email=?, phone=? WHERE id=?',
                 (data['name'], data['email'], data.get('phone', ''), id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Customer updated successfully'})

# DELETE - Delete customer
@app.route('/customers/<int:id>', methods=['DELETE'])
def delete_customer(id):
    conn = sqlite3.connect('customers.db')
    conn.execute('DELETE FROM customers WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Customer deleted successfully'})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)