
from flask import Response
from app import app
import unittest
import os
os.environ['TESTING'] = 'true'


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>Melissa Lam</title>" in html
        # TODO add more tests relating to the home page
        assert "<h2>HELLO!</h2>" in html
        message = "Test value is none."
        self.assertIsNotNone(response, message)

    def test_timeline_post(self):
        response = self.client.post(
            "/api/timeline_post", data={"name": "test", "email": "test@something.com", "content": "timeline"})
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()

        # Tests for POST api
        self.assertIsInstance(json, dict)

    def test_timeline_get(self):
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 0
        self.assertIsInstance(json, dict)

    def test_timeline(self):
        response = self.client.get("/timeline")
        html = response.get_data(as_text=True)
        assert '<button type="submit">Submit</button>' in html

    def test_malformed_timeline_post_name(self):
        response = self.client.post(
            "/api/timeline_post", data={"email": "john@example.com", "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        response_text = response.get_data(as_text=True)
        assert "Invalid name" in response_text

    def test_malformed_timeline_post_email(self):
        response = self.client.post("/api/timeline_post", data={
                                    "name": "John Doe", "email": "not-an-email", "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html

    def test_malformed_timeline_post_content(self):
        malformed_data = {
            "name": "John Doe", "email": "john@example.com", "content": ""
        }
        response = self.client.post(
            "/api/timeline_post", data=malformed_data)
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html
