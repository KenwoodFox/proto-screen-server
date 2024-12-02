from flask import Blueprint

interface_blueprint = Blueprint("interface", __name__)

# Import all Interface routes
from app.endpoints.interface import index
