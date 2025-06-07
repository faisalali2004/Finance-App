from datetime import datetime, timedelta
from collections import defaultdict
from app.models import Transaction
from sqlalchemy import func

def get_total_balance(user_id):
    income = (
        Transaction.query.with_entities(func.sum(Transaction.amount))
        .filter_by(user_id=user_id, type='income')
        .scalar()
    ) or 0

    expense = (
        Transaction.query.with_entities(func.sum(Transaction.amount))
        .filter_by(user_id=user_id, type='expense')
        .scalar()
    ) or 0

    return income - expense


def get_total_spent(user_id):
    spent = (
        Transaction.query.with_entities(func.sum(Transaction.amount))
        .filter_by(user_id=user_id, type='expense')
        .scalar()
    )
    return spent or 0


def get_spending_by_category(user_id):
    # Returns: dict(category: total_spent)
    data = (
        Transaction.query
        .with_entities(Transaction.category, func.sum(Transaction.amount))
        .filter_by(user_id=user_id, type='expense')
        .group_by(Transaction.category)
        .all()
    )
    return {category: float(total) for category, total in data}


def get_spending_trend(user_id, range_type='month'):
    # Returns: dict(date_label: total_spent)
    today = datetime.today()
    trend_data = defaultdict(float)

    if range_type == 'week':
        start_date = today - timedelta(days=6)
        transactions = (
            Transaction.query
            .filter(Transaction.user_id == user_id,
                    Transaction.type == 'expense',
                    Transaction.timestamp >= start_date)
            .all()
        )
        for tx in transactions:
            label = tx.timestamp.strftime('%a')  # Mon, Tue, ...
            trend_data[label] += float(tx.amount)

    elif range_type == 'month':
        start_date = today.replace(day=1)
        transactions = (
            Transaction.query
            .filter(Transaction.user_id == user_id,
                    Transaction.type == 'expense',
                    Transaction.timestamp >= start_date)
            .all()
        )
        for tx in transactions:
            label = tx.timestamp.strftime('%d %b')  # 01 Jun, 02 Jun...
            trend_data[label] += float(tx.amount)

    elif range_type == 'year':
        start_date = today.replace(month=1, day=1)
        transactions = (
            Transaction.query
            .filter(Transaction.user_id == user_id,
                    Transaction.type == 'expense',
                    Transaction.timestamp >= start_date)
            .all()
        )
        for tx in transactions:
            label = tx.timestamp.strftime('%b')  # Jan, Feb, ...
            trend_data[label] += float(tx.amount)

    return dict(trend_data)
