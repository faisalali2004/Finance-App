import os
from flask import Flask, redirect, url_for
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from .extensions import db, login_manager, mail

def create_app():
    basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    app = Flask(
        __name__,
        template_folder=os.path.join(basedir, 'templates'),
        static_folder=os.path.join(basedir, 'static')
    )

    app.config.from_object('config.Config')

    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    Migrate(app, db)
    Bootstrap(app)

    from app.auth import auth_bp
    from app.dashboard import dashboard_bp
    from app.reports import reports_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(reports_bp, url_prefix='/reports')

    @app.route('/')
    def index():
        return redirect(url_for('dashboard.dashboard'))  # Fixed endpoint

    return app