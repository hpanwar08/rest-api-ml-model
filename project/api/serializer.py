from project.api import api
from flask_restplus import fields

sentiment_json = api.model('Sentiment JSON', {
        'text': fields.String(required=True, description='Text to be analyzed')
    }
)
