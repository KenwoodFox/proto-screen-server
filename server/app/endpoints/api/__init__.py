from flask import Blueprint

api_blueprint = Blueprint("api", __name__)

# Import all API endpoints (API)
from app.endpoints.api import checkin, upload, logs, gifs
