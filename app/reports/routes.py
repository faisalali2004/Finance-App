import os
import tempfile
import csv
from flask import request, jsonify, send_file, render_template, redirect, url_for, flash, current_app
from app.reports import reports_bp
from app.reports.alerts import get_all_alerts, get_unread_alerts, mark_alert_as_read, add_alert
from werkzeug.utils import secure_filename

# Dummy function: Replace with your actual DB query for reports
def get_reports_data():
    # Example: Replace with actual DB query
    return [
        {"date": "2025-06-01", "category": "Food", "type": "Expense", "amount": 1500, "description": "Lunch"},
        {"date": "2025-06-02", "category": "Transport", "type": "Expense", "amount": 500, "description": "Bus fare"},
    ]

# Main reports page
@reports_bp.route('/', methods=['GET'])
def reports():
    reports_data = get_reports_data()
    alerts = get_all_alerts()
    has_alerts = bool(get_unread_alerts())
    return render_template(
        'reports/reports.html',
        reports_data=reports_data,
        alerts=alerts,
        has_alerts=has_alerts
    )

# Route for fetching all alerts (API)
@reports_bp.route('/alerts', methods=['GET'])
def fetch_alerts():
    alerts_data = get_all_alerts()
    return jsonify(alerts_data), 200

# Route for fetching unread alerts (API)
@reports_bp.route('/alerts/unread', methods=['GET'])
def fetch_unread_alerts():
    unread_data = get_unread_alerts()
    return jsonify(unread_data), 200

# Route for marking an alert as read (API)
@reports_bp.route('/alerts/read/<int:alert_id>', methods=['POST'])
def mark_alert_as_read_endpoint(alert_id):
    result = mark_alert_as_read(alert_id)
    if "error" in result:
        return jsonify(result), 404
    return jsonify(result), 200

# Route for adding a new alert (API)
@reports_bp.route('/alerts/add', methods=['POST'])
def create_alert():
    message = request.json.get("message")
    if not message:
        return jsonify({"error": "Message is required"}), 400
    result = add_alert(message)
    return jsonify(result), 201

# Route for importing a CSV file (for form POST)
@reports_bp.route('/import_csv', methods=['POST'])
def import_csv_file():
    if 'csv_file' not in request.files:
        flash("No file part", "danger")
        return redirect(url_for('reports.reports'))

    file = request.files['csv_file']
    if file.filename == '':
        flash("No selected file", "danger")
        return redirect(url_for('reports.reports'))

    filename = secure_filename(file.filename)
    temp_path = os.path.join(tempfile.gettempdir(), filename)
    file.save(temp_path)

    # Example: Read and process CSV (replace with your DB logic)
    imported_rows = 0
    with open(temp_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Here you would insert into your DB
            imported_rows += 1
    os.remove(temp_path)
    flash(f"CSV imported successfully! {imported_rows} rows processed.", "success")
    return redirect(url_for('reports.reports'))

# Route for exporting a CSV file (for form GET)
@reports_bp.route('/export_csv', methods=['GET'])
def export_csv_file():
    data = get_reports_data()  # Replace with actual DB query
    if not data:
        flash("No data to export.", "warning")
        return redirect(url_for('reports.reports'))

    # Write to a temporary CSV file
    fd, temp_path = tempfile.mkstemp(suffix='.csv')
    with os.fdopen(fd, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['date', 'category', 'type', 'amount', 'description']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

    return send_file(temp_path, as_attachment=True, download_name='transactions_export.csv')
