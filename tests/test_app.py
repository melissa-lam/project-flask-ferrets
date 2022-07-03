
from flask import Response
import unittest
import os
os.environ['TESTING'] = 'true'

from app import app


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
    
    def test_timeline(self):
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 0

        #tests for POST and GET api endpoints
        post = self.client.post("/api/timeline_post", data=dict({"name": "John Doe", "email": "john@example.com", "content": "Hello world, I\'m John!"}))
        assert post.status_code == 200

        response_2 = self.client.get("/api/timeline_post")
        assert response_2.status_code == 200
        assert response_2.is_json
        json = response_2.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 1

        #Tests for timeline page
        response_3 = self.client.get("/timeline")
        assert response_3.status_code == 200
        html = response_3.get_data(as_text=True)
        assert '<button type="submit">Submit</button>' in html
        self.assertIsNotNone(html)

    # def test_timeline_post(self):
    #     response = self.client.post(
    #         "/api/timeline_post", data={"name": "test", "email": "test@something.com", "content": "timeline"})
    #     assert response.status_code == 200
    #     assert response.is_json
    #     json = response.get_json()
    #     assert len(json["timeline_posts"]) == 1

    #     # Tests for POST api
    #     self.assertIsInstance(json, dict)

    # def test_timeline_get(self):
    #     response = self.client.get("/api/timeline_post")
    #     assert response.status_code == 200
    #     assert response.is_json
    #     json = response.get_json()
    #     assert "timeline_posts" in json
    #     assert len(json["timeline_posts"]) == 0
    #     self.assertIsInstance(json, dict)

    

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
