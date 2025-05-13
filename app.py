from flask import Flask, jsonify, request
from data import products

app = Flask(__name__)

# Homepage route that returns a welcome message
@app.route("/", methods=["GET"])
def home():
    """
    Root endpoint that returns a welcome message.
    
    Returns:
        JSON: A welcome message in JSON format
    """
    return jsonify({
        "message": "Welcome to the Product Catalog API!",
        "endpoints": {
            "all_products": "/products",
            "product_by_id": "/products/<id>",
            "filter_by_category": "/products?category=<category>"
        }
    })

# GET /products route that returns all products or filters by category
@app.route("/products", methods=["GET"])
def get_products():
    """
    Returns all products or filters by category if a query parameter is provided.
    
    Query Parameters:
        category (str): Optional - Filter products by category
        
    Returns:
        JSON: List of products or filtered products
    """
    # Check if category query parameter exists
    category = request.args.get("category")
    
    if category:
        # Filter products by category (case-insensitive)
        filtered_products = [
            product for product in products 
            if product["category"].lower() == category.lower()
        ]
        return jsonify(filtered_products)
    
    # If no category parameter, return all products
    return jsonify(products)

# GET /products/<id> route that returns a specific product by ID or 404
@app.route("/products/<int:id>", methods=["GET"])
def get_product_by_id(id):
    """
    Returns a specific product by ID.
    
    Args:
        id (int): The product ID
        
    Returns:
        JSON: Product information if found, or 404 error if not found
    """
    # Find product with matching ID
    for product in products:
        if product["id"] == id:
            return jsonify(product)
    
    # Return 404 if product with given ID is not found
    return jsonify({"error": "Product not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)