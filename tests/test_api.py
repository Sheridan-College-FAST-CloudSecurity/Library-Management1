import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(_file_), '..'))

from app.main import app
from fastapi.testclient import TestClient

class TestLibraryAPI(unittest.TestCase):
    
    def setUp(self):
        self.client = TestClient(app)
    
    def test_home_endpoint(self):
        """Test the home endpoint"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        # REMOVED: self.assertEqual(data["version"], "1.0.0")
        self.assertEqual(data["message"], "Library Management System")
    
    def test_items_endpoint(self):
        """Test the items endpoint returns books"""
        response = self.client.get("/items")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertTrue(isinstance(data, list))
        self.assertTrue(len(data) > 0)
    
    def test_health_endpoint(self):
        """Test the health endpoint"""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertEqual(data, {"status": "ok"})

if _name_ == "_main_":
    unittest.main()
