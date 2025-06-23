from fastapi.testclient import TestClient
import unittest

from modul_with_tests.max_number_app import app


class TestMaxNumber(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)
        self.base_url = "/max_number/"

    def test_can_correct_max_number_in_series_of_two(self):
        numbers = 1, 2
        url = self.base_url + "/".join(str(i) for i in numbers)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response_text = response.text
        corr_answer_str = f"<i>{max(numbers)}</i>"
        self.assertTrue(corr_answer_str in response_text)

    def test_returns_error_for_non_integer_input(self):
        response = self.client.get("/max_number/10/abc/20")
        self.assertEqual(response.status_code, 400)
        self.assertIn("Все параметры пути должны быть целыми числами", response.text)

