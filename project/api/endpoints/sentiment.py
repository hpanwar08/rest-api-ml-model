from flask import request
from flask_restplus import Resource

from project.api import api
from project.sentiment import model
from project.api.serializer import sentiment_json


ns = api.namespace(name='', description="API for sentiment")


@ns.route("/ping")
class Ping(Resource):
    def get(self):
        """To check if API is up
        """
        return {"status": "success", "message": "pong"}


@ns.route("/sentiment")
class Sentiment(Resource):
    @api.expect(sentiment_json)
    def post(self):
        """Get the predicted sentiment of text
        """
        response_body = {"status": "fail", "message": "invalid json"}
        post_data = request.get_json()
        if not post_data:
            return response_body, 400

        result, probs = model.predict(post_data['text'])
        if probs:
            response_body['status'] = 'success'
            message = {}
            message['text'] = post_data['text']
            message['sentiment'] = 'negative' if result == 0 else 'positive'
            message['confidence'] = float(
                f'{probs[0]:.4f}' if result == 0 else f'{probs[1]:.4f}')

            response_body['message'] = message
            return response_body, 200

        response_body['message'] = 'model error'
        return response_body, 400
