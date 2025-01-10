from flask import send_from_directory, current_app
from app.endpoints.api import api_blueprint


@api_blueprint.route("/gifs/<filename>", methods=["GET"])
def serve_gif(filename):
    current_app.logger.info(f"Serving GIF: {filename}")
    return send_from_directory("/tmp", filename)
