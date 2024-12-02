import logging

from flask import jsonify
from app.endpoints.api import api_blueprint
from app.advanced_logging import memory_log_handler  # Import the global log handler


@api_blueprint.route("/logs", methods=["GET"])
def get_logs():
    """
    Fetch recent logs from the in-memory log stream.
    """

    logs = memory_log_handler.get_logs()
    return jsonify({"logs": logs})
