import os
import logging
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask.logging import default_handler

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = "/tmp/screenserver"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Server metadata
SERVER_VERSION = "1.0.0"
CURRENT_FIRMWARE_VERSION = "1.0.1"

# Track connected screens
connected_screens = {}  # {screen_id: {"name": str, "status": str}}

# Configure Logging
if not app.debug:  # Avoid reconfiguring logging in debug mode
    log_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)

    # File handler
    file_handler = logging.FileHandler("app.log")
    file_handler.setFormatter(log_formatter)

    # Attach handlers to Flask's app logger
    app.logger.addHandler(console_handler)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)


@app.route("/")
def index():
    # Read README for explanation section
    readme_path = os.path.join(os.path.dirname(__file__), "README.md")
    try:
        with open(readme_path, "r") as readme_file:
            readme_content = readme_file.read()
    except FileNotFoundError:
        readme_content = "README file not found. Add a README.md to explain your app."

    return render_template(
        "index.html", screens=len(connected_screens), readme_content=readme_content
    )


@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file and file.filename.lower().endswith(".gif"):
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(file_path)
        app.logger.info(f"Uploaded file: {file.filename}")
        return jsonify({"message": "File uploaded successfully"}), 200

    return jsonify({"error": "Unsupported file type, only .gif allowed"}), 400


@app.route("/checkin", methods=["POST"])
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


@app.route("/logs")
def get_logs():
    # Example log fetching (mocked for now)
    log_file_path = "app.log"
    if os.path.exists(log_file_path):
        with open(log_file_path, "r") as log_file:
            logs = log_file.readlines()
    else:
        logs = ["No logs available."]
    return jsonify(logs)


@app.route("/gifs/<filename>")
def serve_gif(filename):
    app.logger.info(f"Serving GIF: {filename}")
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


if __name__ == "__main__":
    app.logger.info(f"Starting prototype server {os.getenv('VERSION')}")
    app.run(debug=True)
