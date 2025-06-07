# app/extensions.py

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail  # <--- ADD THIS LINE

# Initialize extension instances (not bound to app yet)
db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail() # <--- ADD THIS LINE

# Optional: Customize login behavior
login_manager.login_view = 'auth.login' # THIS IS THE CRUCIAL LINE for the endpoint
login_manager.login_message_category = 'info' # Flash category for login messages

# User loader callback for Flask-Login
# This function is crucial for Flask-Login to load a user from the ID stored in the session.
@login_manager.user_loader
def load_user(user_id):
    # This import needs to be here to avoid circular dependencies
    # The actual User model is defined in app/models.py
    from app.models import User
    # Ensure user_id is an integer for query.get()
    return User.query.get(int(user_id))