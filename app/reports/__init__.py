from flask import Blueprint, render_template

reports_bp = Blueprint('reports', __name__, url_prefix='/reports')

@reports_bp.route('/')
def reports():
    return render_template('reports/reports.html')

