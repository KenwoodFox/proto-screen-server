from flask import request, jsonify, current_app, url_for
from app.endpoints.api import api_blueprint
import time

SERVER_VERSION = "1.0.0"
CURRENT_FIRMWARE_VERSION = "1.0.1"


@api_blueprint.route("/checkin", methods=["POST"])
def checkin():
    """
    API for screens to check in with the server.
    Receives client information and responds with server metadata, including an offered ID, API root, server version, and current time in epoch format.
    """
    try:
        data = request.json

        # Validate the input
        if not data or "screen_name" not in data:
            current_app.logger.warning("Invalid checkin request")
            return jsonify({"error": "Invalid request, 'screen_name' required"}), 400

        # Generate a unique ID for the screen
        screen_name = data["screen_name"]
        screen_id = f"screen_{int(time.time())}"  # Use epoch seconds for a unique ID, maybe do random in the future.

        # Construct the response
        response = {
            "server_version": SERVER_VERSION,
            "firmware_version": CURRENT_FIRMWARE_VERSION,
            "offered_id": screen_id,
            "api_root": url_for("api.checkin", _external=True).replace(
                "/checkin", ""
            ),  # Root of the API
            "time_epoch": int(time.time()),  # Current time in epoch format
        }

        # Log the check-in
        current_app.logger.info(
            f"Screen '{screen_name}' checked in with ID '{screen_id}'"
        )

        return jsonify(response), 200

    except Exception as e:
        current_app.logger.error(f"Error in checkin: {e}")
        return jsonify({"error": "Internal server error"}), 500
