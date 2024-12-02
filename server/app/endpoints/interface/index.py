from flask import render_template, current_app
from app.endpoints.interface import interface_blueprint
import os


@interface_blueprint.route("/", methods=["GET"])
def index():
    readme_path = os.path.join(os.path.dirname(__file__), "../../../README.md")
    try:
        with open(readme_path, "r") as readme_file:
            readme_content = readme_file.read()
    except FileNotFoundError:
        readme_content = "README file not found..."

    screens_count = len(current_app.config.get("connected_screens", {}))
    return render_template(
        "index.html", screens=screens_count, readme_content=readme_content
    )
