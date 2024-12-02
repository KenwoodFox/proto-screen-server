from flask import Flask
from app.endpoints.api import api_blueprint
from app.endpoints.interface import interface_blueprint


def create_app():
    app = Flask(__name__)

    # Configuration
    app.config["UPLOAD_FOLDER"] = "/tmp/screenserver"

    # Ensure upload folder exists
    import os

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # Register blueprints
    app.register_blueprint(api_blueprint, url_prefix="/api")
    app.register_blueprint(interface_blueprint, url_prefix="/")

    return app
