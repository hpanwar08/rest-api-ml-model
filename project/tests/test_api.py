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
        with self.client:
            response = self.client.post(
                '/api/v1/sentiment',
                data=json.dumps({
                    'text': 'tweet'
                }),
                content_type='application/json'
                )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])
            self.assertIn('tweet', data['message'])


if __name__ == "__main__":
    unittest.main()