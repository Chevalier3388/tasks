from fastapi.testclient import TestClient
import unittest

from modul_with_tests.hello_world_with_day import app


class TestHelloWorld(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)
        self.base_url = "/hello_world/"

    def test_can_correct_username(self):
        username = "username"
        response = self.client.get(self.base_url + username)
        self.assertEqual(response.status_code, 200)
        response_text = response.text
        self.assertTrue(username in response_text)
