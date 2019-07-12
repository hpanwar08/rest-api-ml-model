from project.api import api
from flask_restplus import fields

sentiment_json = api.model(
    "Sentiment json",
    {"text": fields.String(
        required=True,
        description="Text to be analyzed")}
)


sentiments_json = api.model(
    "Sentiments json",
    {"texts": fields.List(
        fields.Nested(sentiment_json),
        description="List of text")},
)
