from flask import render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from app.dashboard import dashboard_bp
from app.dashboard.forms import TransactionForm
from app.models import Transaction
from app.extensions import db
from datetime import datetime, timedelta
from sqlalchemy import func
import json

# Utility functions for dashboard data aggregation
def get_total_balance(user_id):
    income = db.session.query(func.sum(Transaction.amount)).filter_by(user_id=user_id, type='income').scalar() or 0
    expenses = db.session.query(func.sum(Transaction.amount)).filter_by(user_id=user_id, type='expense').scalar() or 0
    return income - expenses

def get_total_spent(user_id):
    expenses = db.session.query(func.sum(Transaction.amount)).filter_by(user_id=user_id, type='expense').scalar() or 0
    return expenses

def get_spending_by_category(user_id):
    category_spending = db.session.query(
        Transaction.category,
        func.sum(Transaction.amount)
    ).filter_by(user_id=user_id, type='expense').group_by(Transaction.category).all()
    return {category: float(amount) for category, amount in category_spending if category is not None}

def get_spending_trend(user_id, period='month'):
    data = []
    labels = []
    current_date = datetime.utcnow()

    if period == 'month':
        for i in range(6):
            month_start = (current_date.replace(day=1) - timedelta(days=30*i)).replace(day=1)
            month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
            total_expense = db.session.query(func.sum(Transaction.amount)).filter(
                Transaction.user_id == user_id,
                Transaction.type == 'expense',
                Transaction.date >= month_start,
                Transaction.date <= month_end
            ).scalar() or 0
            labels.insert(0, month_start.strftime('%b %Y'))
            data.insert(0, float(total_expense))
    elif period == 'week':
        for i in range(4):
            week_end = current_date - timedelta(weeks=i)
            week_start = week_end - timedelta(days=week_end.weekday())
            total_expense = db.session.query(func.sum(Transaction.amount)).filter(
                Transaction.user_id == user_id,
                Transaction.type == 'expense',
                Transaction.date >= week_start,
                Transaction.date < week_start + timedelta(weeks=1)
            ).scalar() or 0
            labels.insert(0, f"Week {week_start.isocalendar()[1]}")
            data.insert(0, float(total_expense))
    elif period == 'year':
        for i in range(3):
            year_start = current_date.replace(year=current_date.year - i, month=1, day=1)
            year_end = current_date.replace(year=current_date.year - i, month=12, day=31)
            total_expense = db.session.query(func.sum(Transaction.amount)).filter(
                Transaction.user_id == user_id,
                Transaction.type == 'expense',
                Transaction.date >= year_start,
                Transaction.date <= year_end
            ).scalar() or 0
            labels.insert(0, str(year_start.year))
            data.insert(0, float(total_expense))

    return {'labels': labels, 'data': data}

# Routes
@dashboard_bp.route('/')
@login_required
def dashboard():
    transaction_form = TransactionForm()
    user_id = current_user.id if current_user.is_authenticated else None

    total_balance = get_total_balance(user_id) if user_id else 0.0
    total_spent = get_total_spent(user_id) if user_id else 0.0
    category_data = get_spending_by_category(user_id) if user_id else {}

    monthly_trend = get_spending_trend(user_id, 'month') if user_id else {'labels': [], 'data': []}
    weekly_trend = get_spending_trend(user_id, 'week') if user_id else {'labels': [], 'data': []}
    yearly_trend = get_spending_trend(user_id, 'year') if user_id else {'labels': [], 'data': []}

    pie_chart_labels = list(category_data.keys())
    pie_chart_data = list(category_data.values())

    return render_template(
        'dashboard/index.html',
        total_balance=f"{total_balance:,.2f}",
        total_spent=f"{total_spent:,.2f}",
        pie_chart_data=json.dumps(pie_chart_data),
        pie_chart_labels=json.dumps(pie_chart_labels),
        line_chart_data=json.dumps(monthly_trend['data']),
        line_chart_labels=json.dumps(monthly_trend['labels']),
        line_chart_weekly_data=json.dumps(weekly_trend['data']),
        line_chart_weekly_labels=json.dumps(weekly_trend['labels']),
        line_chart_yearly_data=json.dumps(yearly_trend['data']),
        line_chart_yearly_labels=json.dumps(yearly_trend['labels']),
        transaction_form=transaction_form
    )

@dashboard_bp.route('/add_transaction', methods=['POST'])
@login_required
def add_transaction():
    form = TransactionForm()
    if form.validate_on_submit():
        description_data = form.description.data if form.description.data else None

        new_tx = Transaction(
            user_id=current_user.id,
            amount=form.amount.data,
            category=form.category.data,
            type=form.type.data,
            description=description_data
        )
        db.session.add(new_tx)
        db.session.commit()
        flash(f"{form.type.data.capitalize()} added successfully.", "success")
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in {field}: {error}", 'danger')
        flash("Please correct the errors in the form.", "danger")

    return redirect(url_for('dashboard.dashboard'))
