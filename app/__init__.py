
from flask import Flask, jsonify
from prometheus_client import Counter, generate_latest
from prometheus_client import CONTENT_TYPE_LATEST

app = Flask(__name__)

REQUEST_COUNT = Counter(
    "ecommerce_requests_total",
    "Total number of application requests"
)

PRODUCTS = [
    {
        "id": 1,
        "name": "Laptop",
        "price": 55000,
        "category": "Electronics"
    },
    {
        "id": 2,
        "name": "Headphones",
        "price": 2500,
        "category": "Electronics"
    },
    {
        "id": 3,
        "name": "Backpack",
        "price": 1200,
        "category": "Accessories"
    }
]


@app.before_request
def count_requests():
    REQUEST_COUNT.inc()


@app.route("/")
def home():
    return jsonify({
        "application": "Online Shopping and Order Management System",
        "status": "running",
        "version": "1.0.0",
        "message": "Welcome to the DevOps project"
    })


@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200


@app.route("/products")
def get_products():
    return jsonify(PRODUCTS), 200


@app.route("/products/<int:product_id>")
def get_product(product_id):
    product = next(
        (p for p in PRODUCTS if p["id"] == product_id),
        None
    )

    if product is None:
        return jsonify({"error": "Product not found"}), 404

    return jsonify(product), 200


@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {
        "Content-Type": CONTENT_TYPE_LATEST
    }
