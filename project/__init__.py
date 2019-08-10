import os
from flask import Flask, Blueprint
from project.api.endpoints.restplus import api


def create_app(script_info=None):
    app = Flask(__name__)
    # app_settings = os.getenv("APP_SETTINGS")
    # app.config.from_object(app_settings)

    from project.api.endpoints.sentiment import ns as sentiment_blueprint

    api_blueprint = Blueprint("api", __name__, url_prefix="/api/v1")
    api.init_app(api_blueprint)
    app.register_blueprint(api_blueprint)
    api.add_namespace(sentiment_blueprint)

    return app
