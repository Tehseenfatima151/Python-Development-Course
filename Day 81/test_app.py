"""
Automated Test Suite for House Price Predictor Application
Tests Flask multi-page web routes, validation logic, ML inference, and REST API endpoints.
"""

import unittest
import json
from app import app, format_pakistani_crore, format_currency_pkr


class HousePricePredictorTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()

    def test_currency_formatting(self):
        """Test PKR and Crore/Lacs conversion logic."""
        self.assertEqual(format_currency_pkr(18500000), "PKR 18,500,000")
        self.assertEqual(format_pakistani_crore(18500000), "PKR 1.85 Crore")
        self.assertEqual(format_pakistani_crore(850000), "PKR 8.50 Lacs")
        self.assertEqual(format_pakistani_crore(50000), "PKR 50,000")

    def test_index_route(self):
        """Test GET / marketing landing page."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"PropVal.AI", response.data)
        self.assertIn(b"AI-Powered", response.data)
        self.assertIn(b"Start Property Valuation", response.data)

    def test_valuation_route(self):
        """Test GET /valuation dedicated application page."""
        response = self.client.get('/valuation')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"AI Property Valuation", response.data)
        self.assertIn(b"Lahore", response.data)

    def test_how_it_works_route(self):
        """Test GET /how-it-works pipeline explanation page."""
        response = self.client.get('/how-it-works')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"How PropVal.AI Works", response.data)
        self.assertIn(b"ColumnTransformer", response.data)

    def test_insights_route(self):
        """Test GET /insights analytics dashboard."""
        response = self.client.get('/insights')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Model Insights & Analytics", response.data)
        self.assertIn(b"Regression Model Comparison", response.data)
        self.assertIn(b"Random Forest", response.data)

    def test_market_trends_route(self):
        """Test GET /market-trends dataset analytics page."""
        response = self.client.get('/market-trends')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Pakistan Property Market Insights", response.data)
        self.assertIn(b"Dataset-Based Market Insights Disclosure", response.data)

    def test_api_docs_route(self):
        """Test GET /api-docs developer documentation page."""
        response = self.client.get('/api-docs')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"PropVal.AI REST API", response.data)
        self.assertIn(b"POST /api/predict", response.data)

    def test_about_route(self):
        """Test GET /about platform information page."""
        response = self.client.get('/about')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"The Intelligence Behind PropVal.AI", response.data)
        self.assertIn(b"Synthetic Dataset Disclosure", response.data)

    def test_predict_form_valid(self):
        """Test POST /predict with valid HTML form data."""
        form_data = {
            "sqft": "1800",
            "bedrooms": "3",
            "bathrooms": "2",
            "location": "Lahore"
        }
        response = self.client.post('/predict', data=form_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Estimated Property Value", response.data)
        self.assertIn(b"PKR", response.data)
        self.assertIn(b"Lahore", response.data)

    def test_predict_form_invalid_location(self):
        """Test POST /predict with invalid location triggers redirect/error."""
        form_data = {
            "sqft": "1800",
            "bedrooms": "3",
            "bathrooms": "2",
            "location": "AtlantisCity"
        }
        response = self.client.post('/predict', data=form_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Location &#39;AtlantisCity&#39; is unsupported", response.data)

    def test_api_predict_valid(self):
        """Test POST /api/predict with valid JSON payload."""
        payload = {
            "sqft": 2720,
            "bedrooms": 4,
            "bathrooms": 3,
            "location": "Islamabad"
        }
        response = self.client.post(
            '/api/predict',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        
        self.assertTrue(data['success'])
        self.assertIn("predicted_price", data)
        self.assertIn("formatted_price", data)
        self.assertIn("formatted_crore", data)
        self.assertEqual(data["currency"], "PKR")
        self.assertGreater(data["predicted_price"], 1000000)

    def test_api_predict_missing_fields(self):
        """Test POST /api/predict with missing required fields."""
        payload = {
            "sqft": 1800,
            "bedrooms": 3
        }
        response = self.client.post(
            '/api/predict',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data.decode('utf-8'))
        self.assertFalse(data['success'])
        self.assertIn("error", data)

    def test_api_predict_negative_sqft(self):
        """Test POST /api/predict with negative square footage."""
        payload = {
            "sqft": -500,
            "bedrooms": 3,
            "bathrooms": 2,
            "location": "Karachi"
        }
        response = self.client.post(
            '/api/predict',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data.decode('utf-8'))
        self.assertFalse(data['success'])
        self.assertIn("Area must be between", data['error'])

    def test_api_predict_unsupported_location(self):
        """Test POST /api/predict with unsupported city."""
        payload = {
            "sqft": 1500,
            "bedrooms": 3,
            "bathrooms": 2,
            "location": "Tokyo"
        }
        response = self.client.post(
            '/api/predict',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data.decode('utf-8'))
        self.assertFalse(data['success'])
        self.assertIn("unsupported", data['error'])

    def test_404_handling(self):
        """Test 404 handler for HTML and API routes."""
        html_resp = self.client.get('/random-nonexistent-url')
        self.assertEqual(html_resp.status_code, 404)
        self.assertIn(b"404 - Page Not Found", html_resp.data)

        api_resp = self.client.get('/api/random-nonexistent-endpoint')
        self.assertEqual(api_resp.status_code, 404)
        api_data = json.loads(api_resp.data.decode('utf-8'))
        self.assertFalse(api_data['success'])


if __name__ == '__main__':
    unittest.main()
