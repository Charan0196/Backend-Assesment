from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)

# Load customers data
def load_customers():
    with open('data/customers.json', 'r') as f:
        return json.load(f)

customers = load_customers()

@app.route('/api/health')
def health():
    return jsonify({"status": "healthy"})

@app.route('/api/customers')
def get_customers():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    
    start = (page - 1) * limit
    end = start + limit
    
    paginated = customers[start:end]
    
    return jsonify({
        "data": paginated,
        "total": len(customers),
        "page": page,
        "limit": limit
    })

@app.route('/api/customers/<customer_id>')
def get_customer(customer_id):
    for customer in customers:
        if customer['customer_id'] == customer_id:
            return jsonify(customer)
    return jsonify({"error": "Customer not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
