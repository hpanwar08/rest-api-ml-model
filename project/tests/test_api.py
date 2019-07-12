import unittest
import json

from project.tests.base import BaseTestCase


class TestSentimentService(BaseTestCase):
    def test_ping(self):
        """Ensure /ping route behaves correctly
        """
        with self.client:
            response = self.client.get("/api/v1/ping")
            data = json.loads(response.data.decode())
            self.assertIn("success", data["status"])
            self.assertIn("pong", data["message"])

    def test_sentiment(self):
        """Ensure /sentiment works
        """
        with self.client:
            response = self.client.post(
                "/api/v1/sentiment",
                data=json.dumps({"text": "i am so happy"}),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn("success", data["status"])
            self.assertIn("positive", data["message"]["sentiment"])

    def test_invalid_sentiment_json(self):
        """Ensure proper message is returned for invalid json
        """
        with self.client:
            response = self.client.post(
                "/api/v1/sentiment",
                data=json.dumps({"aabb": "i am so happy"}),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn("fail", data["status"])
            self.assertIn("invalid json", data["message"])

    def test_invalid_sentiment_text(self):
        """Ensure proper message is returned for invalid text
        """
        with self.client:
            response = self.client.post(
                "/api/v1/sentiment",
                data=json.dumps({"text": 1234}),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn("fail", data["status"])
            self.assertIn("text should be string", data["message"])

    def test_sentiments(self):
        """Ensure /sentiments works
        """
        with self.client:
            response = self.client.post(
                "/api/v1/sentiments",
                data=json.dumps(
                    {"texts": [
                        {"text": "I am happy"},
                        {"text": "i am so sad"}
                    ]}
                ),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn("success", data["status"])
            self.assertIn("positive", data["message"][0]["sentiment"])
            self.assertIn("negative", data["message"][1]["sentiment"])

    def test_invalid_sentiments_json(self):
        """Ensure proper message is returned for invalid json
        """
        with self.client:
            response = self.client.post(
                "/api/v1/sentiment",
                data=json.dumps(
                    {"abcd": [
                        {"text": "I am happy"},
                        {"text": "i am so sad"}
                    ]}
                ),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn("fail", data["status"])
            self.assertIn("invalid json", data["message"])

    def test_invalid_sentiments_text(self):
        """Ensure proper message is returned for invalid text
        """
        with self.client:
            response = self.client.post(
                "/api/v1/sentiments",
                data=json.dumps(
                    {"texts": [
                        {"text": 1212},
                        {"text": "i am so sad"}
                    ]}
                ),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn("partial fail", data["status"])
            self.assertIn("fail", data["message"][0]["status"])
            self.assertIn(
                "text should be string", 
                data["message"][0]["message"]
            )
            self.assertIn("negative", data["message"][1]["sentiment"])

    def test_invalid_sentiments_json_array(self):
        """Ensure proper message is returned for invalid json array
        """
        with self.client:
            response = self.client.post(
                "/api/v1/sentiments",
                data=json.dumps({"texts": {"text": "i am so sad"}}),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn("fail", data["status"])
            self.assertIn("texts should be array", data["message"])


if __name__ == "__main__":
    unittest.main()
