import os
from flask import request, jsonify, send_file
from app.reports import reports_bp
from app.reports.alerts import get_all_alerts, get_unread_alerts, mark_alert_as_read, add_alert
from app.reports.import_export import import_csv, export_csv

# Route for fetching all alerts
@reports_bp.route('/alerts', methods=['GET'])
def fetch_alerts():
    """Fetch and return all alerts."""
    alerts_data = get_all_alerts()
    return jsonify(alerts_data), 200

# Route for fetching unread alerts
@reports_bp.route('/alerts/unread', methods=['GET'])
def fetch_unread_alerts():
    """Fetch and return unread alerts."""
    unread_data = get_unread_alerts()
    return jsonify(unread_data), 200

# Route for marking an alert as read
@reports_bp.route('/alerts/read/<int:alert_id>', methods=['POST'])
def mark_alert_as_read_endpoint(alert_id):
    """Mark a specific alert as read."""
    result = mark_alert_as_read(alert_id)
    if "error" in result:
        return jsonify(result), 404
    return jsonify(result), 200

# Route for adding a new alert
@reports_bp.route('/alerts/add', methods=['POST'])
def create_alert():
    """Add a new alert."""
    message = request.json.get("message")
    if not message:
        return jsonify({"error": "Message is required"}), 400
    result = add_alert(message)
    return jsonify(result), 201

# Route for importing a CSV file
@reports_bp.route('/import', methods=['POST'])
def import_csv_file():
    """Handle CSV file import."""
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    result, status_code = import_csv(file)
    return jsonify(result), status_code

# Route for exporting a CSV file
@reports_bp.route('/export', methods=['GET'])
def export_csv_file():
    """Handle CSV file export."""
    # Example data (replace with actual database query results)
    data = [
        {"Date": "2025-06-01", "Category": "Food", "Amount": 1500},
        {"Date": "2025-06-02", "Category": "Transport", "Amount": 500},
    ]
    filename = 'transactions_export.csv'
    result, status_code = export_csv(data, filename)
    if status_code == 200:
        file_path = result.get("file_path")
        return send_file(file_path, as_attachment=True)
    return jsonify(result), status_code
