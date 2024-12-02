import logging

from flask import Flask
from app.endpoints.api import api_blueprint
from app.endpoints.interface import interface_blueprint

from app.advanced_logging import MemoryLogHandler, memory_log_handler


def create_app():
    app = Flask(__name__)

    # Configuration
    app.config["UPLOAD_FOLDER"] = "/tmp/screenserver"

    # Configure the global logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)  # Set root logger level
    root_logger.addHandler(memory_log_handler)

    # Add a formatter for logs
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    memory_log_handler.setFormatter(formatter)

    # Ensure upload folder exists
    import os

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # Register blueprints
    app.register_blueprint(api_blueprint, url_prefix="/api")
    app.register_blueprint(interface_blueprint, url_prefix="/")

    logging.info(f"Built test server.")

    return app
