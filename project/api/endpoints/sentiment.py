from flask import request
from flask_restplus import Resource

from project.api.endpoints.restplus import api


ns = api.namespace(name='/', description="API for sentiment")


@ns.route("/ping")
class Ping(Resource):
    def get(self):
        """To check if API is up
        """
        return {"status": "success", "message": "pong"}


@ns.route("/sentiment")
class Sentiment(Resource):
    def post(self):
        """Get the predicted sentiment of text
        """
        response_body = {"status": "fail", "message": "invalid json"}
        post_data = request.get_json()
        # print(post_data)
        if not post_data:
            return response_body, 400
        response_body['status'] = 'success'
        response_body['message'] = post_data['text']
        return response_body, 200
