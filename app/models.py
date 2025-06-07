# app/models.py

from app.extensions import db # <--- THIS LINE IMPORTS THE INITIALIZED 'db' OBJECT
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    """
    User model for authentication and linking transactions.
    Includes methods for password hashing.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    # Relationship to transactions
    transactions = db.relationship('Transaction', backref='user', lazy=True)

    def set_password(self, password):
        """Hashes the password and stores it."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Checks if the provided password matches the hashed password."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Transaction(db.Model):
    """
    Transaction model to store income and expenses.
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(10), nullable=False) # 'income' or 'expense'
    category = db.Column(db.String(50), nullable=True) # e.g., 'Salary', 'Food', 'Transport'
    description = db.Column(db.String(200), nullable=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<Transaction {self.type}: {self.amount} on {self.date.strftime("%Y-%m-%d")}>'

