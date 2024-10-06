import json
from flask import Flask, request, jsonify
from product import Product
from productService import ProductService
from recommendationService import RecommendationService

app = Flask(__name__)

def load_products_from_json(file_path):
    with open(file_path, 'r') as file:
        products_data = json.load(file)
        return [Product(**product) for product in products_data]

product_list = load_products_from_json('products.json')
product_service = ProductService(product_list)
recommendation_service = RecommendationService(product_service)

@app.route('/recommendations', methods=['GET'])
def get_recommendations():
    product_id = request.args.get('product_id')
    if not product_id:
        return jsonify({"error": "Product ID is required"}), 400

    selected_product = product_service.find_product_by_id(product_id)
    if not selected_product:
        return jsonify({"error": "Product not found"}), 404

    recommended_products = recommendation_service.get_recommended_products(selected_product)
    recommended_products_json = [
        {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "picture": product.picture,
            "priceUsd": product.priceUsd,
            "categories": product.categories
        }
        for product in recommended_products
    ]
    return jsonify(recommended_products_json)

if __name__ == "__main__":
    app.run(debug=True, port=8001)