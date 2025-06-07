from flask import Blueprint

# Define the blueprint
auth_bp = Blueprint('auth', __name__, template_folder='templates')

# Import routes after defining the blueprint to avoid circular imports
from . import routes
