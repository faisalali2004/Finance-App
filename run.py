# run.py

import os
from app import create_app, db
from app.models import User, Transaction # Import your models for shell context

# Load configuration based on environment
# You can set FLASK_CONFIG='development' or 'production' in your environment variables
# For example: export FLASK_CONFIG=development
config_name = os.environ.get('FLASK_CONFIG', 'development') # Default to development

# Create the Flask application instance
app = create_app()

# Optional: Add a shell context for Flask-CLI
# This allows you to interact with your database models easily in the Flask shell
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Transaction=Transaction) # Add all your models here

if __name__ == '__main__':
    # Run the Flask development server
    # In a production environment, you would use a production-ready WSGI server like Gunicorn or uWSGI
    app.run(debug=True) # debug=True is for development, set to False in production
