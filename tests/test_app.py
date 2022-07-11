# tests/test_app.py

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
        assert "<title>Team Jungle Portfolio</title>" in html
        # Add more tests relating to home page
        assert '<h1>Welcome to&nbsp<span class="txt-type blink" data-wait="1500" data-words=\'["the", "Magnificent", "Mustafa", "Team Jungle"]\'></span></h1>' in html
        assert "<h2>MLH fellowship hackathon portfolio</h2>" in html
        assert "<h1 class=\"hidden\">Welcome to&nbspTeam Jungle!!</h1>" in html

    def test_timeline(self):
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 0

        # Add more tests relating to the /api/timeline_post GET and POST apis
        post_response = self.client.post("/api/timeline_post", data={
            "name": "John Doe", 
            "email": "john@example.com", 
            "content": "Hello world! I'm John!"
        })
        assert post_response.status_code == 200
        get_response = self.client.get("/api/timeline_post")
        assert get_response.status_code == 200
        assert get_response.is_json
        g_json = get_response.get_json()
        assert "timeline_posts" in g_json
        assert len(g_json["timeline_posts"]) == 1
        assert g_json["timeline_posts"][0]["name"] == "John Doe"

        # Add more tests relating to the timeline page
        page_response = self.client.get("/timeline")
        assert page_response.status_code == 200
        html = page_response.get_data(as_text=True)
        assert '<input type="text" id="fname" name="name" value="Mustafa Abdulrahman">' in html
        assert '<input type="text" id="lname" name="email" value="mus2003.abdul@gmail.com">' in html
        assert '<textarea rows="4" cols="50" name="content">At w3schools.com you will learn how to make a website. They offer free tutorials in all web development technologies.</textarea>' in html
        assert '<button type="submit">Submit timeline</button>' in html
        assert '<h5 class="card-title">${post.name}: ${post.email}</h5>' in html
        assert '<p class="card-text">${post.content}</p>' in html

    def test_malformed_timeline_post(self):
        # POST request missing name
        response = self.client.post("/api/timeline_post", data={
            "email": "john@example.com", "content": "Hello world! I'm John!"
        })
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid name" in html

        # POST request with empty content
        response = self.client.post("/api/timeline_post", data={
            "name": "John Doe", "email": "john@example.com", "content": ""
        })
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html

        # POST request with malformed email
        response = self.client.post("/api/timeline_post", data={
            "name": "John Doe", "email": "not-an-email", "content": "Hello world! I'm John!"
        })
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html
