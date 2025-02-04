import unittest
from main import app

class TestRoutes(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_index(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_google_calendar(self):
        response = self.client.get("/google-calendar")
        self.assertIn("error", response.get_json())

    def test_ms_calendar(self):
        response = self.client.get("/ms-calendar")
        self.assertIn("error", response.get_json())
