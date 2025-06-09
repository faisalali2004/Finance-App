from flask import Blueprint

reports_bp = Blueprint('reports', __name__, template_folder='templates/reports')

from . import routes  # <-- Make sure this line exists