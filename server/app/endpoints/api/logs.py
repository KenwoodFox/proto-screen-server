from flask import jsonify, current_app
from app.endpoints.api import api_blueprint
import os


@api_blueprint.route("/logs", methods=["GET"])
def get_logs():
    # Example log fetching (Kinda clumsy for now)
    log_file_path = "app.log"
    if os.path.exists(log_file_path):
        with open(log_file_path, "r") as log_file:
            logs = log_file.readlines()
    else:
        logs = ["No logs available."]
    return jsonify(logs)
