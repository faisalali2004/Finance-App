from decimal import Decimal

def format_currency(value):
    """Formats a numeric value into currency format with Rs."""
    try:
        amount = Decimal(value)
        return f"Rs. {amount:,.2f}"
    except Exception:
        return "N/A"

def calculate_totals(transactions):
    """
    Splits and calculates total balance and total spent.
    
    Args:
        transactions (list): List of transaction dicts or objects
    
    Returns:
        dict: {'total_balance': Rs..., 'total_spent': Rs...}
    """
    total_income = Decimal(0)
    total_expense = Decimal(0)

    for tx in transactions:
        if tx.get('type') == 'income':
            total_income += Decimal(tx.get('amount', 0))
        elif tx.get('type') == 'expense':
            total_expense += Decimal(tx.get('amount', 0))

    total_balance = total_income - total_expense

    return {
        'total_balance': format_currency(total_balance),
        'total_spent': format_currency(total_expense)
    }

def prepare_chart_data(transactions):
    """
    Converts transaction list into chart data dicts.
    
    Returns:
        {
            'category_totals': { 'Food': 1200, 'Transport': 300, ... },
            'trend_data': [ {'date': '2025-06-01', 'amount': 400}, ... ]
        }
    """
    from collections import defaultdict
    import datetime

    category_totals = defaultdict(Decimal)
    trend_data = defaultdict(Decimal)

    for tx in transactions:
        amount = Decimal(tx.get('amount', 0))
        category = tx.get('category', 'Uncategorized')
        date = tx.get('date')

        category_totals[category] += amount

        if date:
            date_key = date.strftime('%Y-%m-%d') if isinstance(date, datetime.date) else str(date)
            trend_data[date_key] += amount

    return {
        'category_totals': dict(category_totals),
        'trend_data': dict(trend_data)
    }
