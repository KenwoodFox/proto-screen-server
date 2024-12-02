from flask import request, jsonify, current_app
from app.endpoints.api import api_blueprint

connected_screens = {}  # Keep track of connected screens (MOVE ME)

SERVER_VERSION = "1.0.0"
CURRENT_FIRMWARE_VERSION = "1.0.1"


@api_blueprint.route("/checkin", methods=["POST"])
def checkin():
    """
    API for screens to check in with the server.
    Receives client information and responds with server metadata and an assigned ID.
    """

    try:
        data = request.json
        if not data or "screen_name" not in data:
            app.logger.warning("Invalid checkin request")
            return jsonify({"error": "Invalid request, 'screen_name' required"}), 400

        screen_name = data["screen_name"]

        # Generate a unique ID for the screen
        screen_id = f"screen_{len(connected_screens) + 1}"

        # Add the screen to the connected_screens dictionary
        connected_screens[screen_id] = {"name": screen_name, "status": "initialized"}

        app.logger.info(f"Screen '{screen_name}' checked in as {screen_id}")

        # Respond with server metadata and assigned ID
        response = {
            "server_version": SERVER_VERSION,
            "firmware_version": CURRENT_FIRMWARE_VERSION,
            "screen_id": screen_id,
        }
        return jsonify(response), 200

    except Exception as e:
        app.logger.error(f"Error in checkin: {e}")
        return jsonify({"error": "Internal server error"}), 500
