import unittest
import json
from main import app, product_service, recommendation_service

class RecommendationServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_get_recommendations_no_product_id(self):
        response = self.app.get('/recommendations')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "Product ID is required"})

    def test_get_recommendations_product_not_found(self):
        response = self.app.get('/recommendations', query_string={'product_id': 'nonexistent'})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"error": "Product not found"})

    def test_get_recommendations_success(self):
        response = self.app.get('/recommendations', query_string={'product_id': 'OLJCESPC7Z'})
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        if response.json:
            self.assertIn("id", response.json[0])
            self.assertIn("name", response.json[0])
            self.assertIn("description", response.json[0])
            self.assertIn("picture", response.json[0])
            self.assertIn("priceUsd", response.json[0])
            self.assertIn("categories", response.json[0])

if __name__ == '__main__':
    unittest.main()