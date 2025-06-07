import os
from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from .extensions import db, login_manager

def create_app():
    # Base directory
    basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    # Initialize Flask app
    app = Flask(
        __name__,
        template_folder=os.path.join(basedir, 'templates'),
        static_folder=os.path.join(basedir, 'static')
    )

    # Load configuration
    app.config.from_object('config.Config')

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    Migrate(app, db)
    Bootstrap(app)

    # Flask-Login user loader
    from .models import User  # Import User model
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    # Register blueprints
    from app.auth import auth_bp
    from app.dashboard import dashboard_bp
    from app.reports import reports_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(reports_bp, url_prefix='/reports')

    # Default route redirects to dashboard
    @app.route('/')
    def index():
        return redirect(url_for('dashboard.dashboard'))


    return app
