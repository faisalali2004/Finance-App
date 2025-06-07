from flask import Blueprint

# Define the blueprint for the dashboard module
dashboard_bp = Blueprint('dashboard', __name__, template_folder='templates')

# Import routes at the end to avoid circular imports
from app.dashboard import routes
