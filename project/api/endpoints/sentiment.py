import logging
from flask import request
from flask_restplus import Resource

from project.api import api
from project.sentiment import model
from project.api.serializer import sentiment_json, sentiments_json
from constants import Constants


ns = api.namespace(name="/", description="API for sentiment")
logger = logging.getLogger(Constants.MICROSERVICE_NAME)


@ns.route("/ping")
class Ping(Resource):
    def get(self):
        """To check if API is up
        """
        logger.debug(f'/ping endpoint called')
        return {"status": "success", "message": "pong"}


@ns.route("/sentiment")
class Sentiment(Resource):
    @api.expect(sentiment_json)
    def post(self):
        """Get the predicted sentiment of text
        """
        logger.debug(f'/sentiment endpoint called')
        response_body = {"status": "fail", "message": "invalid json"}
        post_data = request.get_json()
        logger.debug(f'post data {post_data}')

        if not post_data or ("text" not in post_data):
            logger.info(f'invalid json')
            return response_body, 400

        if not isinstance(post_data["text"], str):
            response_body["message"] = "text should be string"
            logger.info(f"text should be string")
            return response_body, 400

        result, probs = model.predict(post_data["text"])
        if probs:
            response_body["status"] = "success"
            message = {}
            message["text"] = post_data["text"]
            message["sentiment"] = "negative" if result == 0 else "positive"
            message["confidence"] = float(
                f"{probs[0]:.4f}" if result == 0 else f"{probs[1]:.4f}"
            )

            response_body["message"] = message
            return response_body, 200

        response_body["message"] = "model error"
        return response_body, 400


@ns.route("/sentiments")
class Sentiments(Resource):
    @api.expect(sentiments_json)
    def post(self):
        """Bulk sentiment prediction
        """
        response_body = {"status": "fail", "message": "invalid json"}
        post_data = request.get_json()
        if not post_data or ("texts" not in post_data):
            logger.info(f"invalid json")
            return response_body, 400

        if not isinstance(post_data["texts"], list):
            response_body["message"] = "texts should be array"
            logger.info(f"texts should be array")
            return response_body, 400

        res = []
        total_texts = len(post_data["texts"])
        total_success = 0
        for text in post_data["texts"]:
            message = {}
            if not isinstance(text["text"], str):
                message["status"] = "fail"
                message["text"] = text["text"]
                message["message"] = "text should be string"
                res.append(message)
                continue

            result, probs = model.predict(text["text"])
            if probs:
                total_success += 1
                message["status"] = "success"
                message["text"] = text["text"]
                message["sentiment"] = \
                    "negative" if result == 0 else "positive"
                message["confidence"] = float(
                    f"{probs[0]:.4f}" if result == 0 else f"{probs[1]:.4f}"
                )
            else:
                message["status"] = "fail"
                message["text"] = text["text"]
            res.append(message)

        if total_success > 0:
            response_body["status"] = "partial fail"
        if total_success == total_texts:
            response_body["status"] = "success"

        response_body["message"] = res
        return response_body, 200
