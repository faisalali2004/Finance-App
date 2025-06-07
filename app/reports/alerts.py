from flask import jsonify
from datetime import datetime

# In-memory alerts storage (replace with database queries in production)
alerts_storage = [
    {"id": 1, "message": "Low balance warning!", "read": False, "timestamp": "2025-06-01 10:00:00"},
    {"id": 2, "message": "Spending threshold exceeded", "read": True, "timestamp": "2025-06-02 14:30:00"},
]

def get_all_alerts():
    """Fetch all alerts."""
    return alerts_storage

def get_unread_alerts():
    """Fetch unread alerts."""
    return [alert for alert in alerts_storage if not alert["read"]]

def mark_alert_as_read(alert_id):
    """Mark an alert as read."""
    for alert in alerts_storage:
        if alert["id"] == alert_id:
            alert["read"] = True
            return {"message": "Alert marked as read", "alert": alert}
    return {"error": "Alert not found"}

def add_alert(message):
    """Add a new alert."""
    new_alert = {
        "id": len(alerts_storage) + 1,
        "message": message,
        "read": False,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    alerts_storage.append(new_alert)
    return {"message": "Alert added successfully", "alert": new_alert}
