from flask import request, jsonify, current_app
from app.endpoints.api import api_blueprint
import os


@api_blueprint.route("/upload", methods=["POST"])
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
