import os
import csv
from flask import jsonify
from werkzeug.utils import secure_filename

# Configuration
UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../uploads')
EXPORT_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../exports')
ALLOWED_EXTENSIONS = {'csv'}

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(EXPORT_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Check if a file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def import_csv(file):
    """Import data from a CSV file."""
    if not allowed_file(file.filename):
        return {"error": "Invalid file format"}, 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    imported_data = []
    try:
        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                imported_data.append(row)
                # Here, you could add code to save each row to the database
    except Exception as e:
        return {"error": f"Failed to process file: {str(e)}"}, 500

    return {"message": "File imported successfully", "data": imported_data}, 200

def export_csv(data, filename='export.csv'):
    """Export data to a CSV file."""
    file_path = os.path.join(EXPORT_FOLDER, filename)
    fieldnames = data[0].keys() if data else []

    try:
        with open(file_path, mode='w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
    except Exception as e:
        return {"error": f"Failed to export file: {str(e)}"}, 500

    return {"message": "File exported successfully", "file_path": file_path}, 200
