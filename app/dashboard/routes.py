from flask import render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from app.dashboard import dashboard_bp
from app.dashboard.forms import TransactionForm
from app.models import Transaction, Account, Category
from app.extensions import db
from collections import defaultdict
from datetime import datetime
from dateutil.relativedelta import relativedelta

@dashboard_bp.route('/')
@login_required
def dashboard():
    accounts = Account.query.filter_by(user_id=current_user.id).all()
    categories = Category.query.filter_by(user_id=current_user.id).all()
    transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.date.desc()).all()

    # Calculate balances for each account
    account_balances = {}
    for account in accounts:
        income = sum(t.amount for t in transactions if t.account_id == account.id and t.type == 'income')
        expense = sum(t.amount for t in transactions if t.account_id == account.id and t.type == 'expense')
        account_balances[account.id] = income - expense

    # Summary
    total_income = sum(t.amount for t in transactions if t.type == 'income')
    total_expense = sum(t.amount for t in transactions if t.type == 'expense')
    total_balance = total_income - total_expense

    # Recent transactions (last 10)
    recent_transactions = transactions[:10]

    # Pie chart: Expenses by category
    expense_by_cat = defaultdict(float)
    for t in transactions:
        if t.type == 'expense':
            expense_by_cat[t.category] += t.amount
    expense_categories_labels = list(expense_by_cat.keys())
    expense_amounts = list(expense_by_cat.values())

    # Bar chart: Income & Expenses by month (last 6 months)
    now = datetime.now()
    chart_labels = []
    chart_income = []
    chart_expense = []
    for i in range(5, -1, -1):
        month = (now - relativedelta(months=i)).strftime('%b %Y')
        chart_labels.append(month)
        month_income = sum(
            t.amount for t in transactions
            if t.type == 'income' and t.date.strftime('%b %Y') == month
        )
        month_expense = sum(
            t.amount for t in transactions
            if t.type == 'expense' and t.date.strftime('%b %Y') == month
        )
        chart_income.append(month_income)
        chart_expense.append(month_expense)

    # Separate categories for income and expense
    income_categories = [(c.name, c.name) for c in categories if c.type == 'income']
    expense_categories = [(c.name, c.name) for c in categories if c.type == 'expense']

    transaction_form = TransactionForm()
    transaction_form.account_id.choices = [
        (a.id, f"{a.name} (Balance: Rs {account_balances[a.id]:.2f})") for a in accounts
    ] + [(-1, "+ Add another account")]
    # Default to expense categories for the expense modal, income for income modal
    transaction_form.category.choices = expense_categories + [("add_category", "+ Add new category")]

    return render_template(
        'dashboard/index.html',
        accounts=accounts,
        account_balances=account_balances,
        categories=categories,
        transaction_form=transaction_form,
        total_income=total_income,
        total_expense=total_expense,
        total_balance=total_balance,
        recent_transactions=recent_transactions,
        expense_categories_labels=expense_categories_labels,
        expense_amounts=expense_amounts,
        chart_labels=chart_labels,
        chart_income=chart_income,
        chart_expense=chart_expense,
        income_categories=income_categories,
        expense_categories=expense_categories
    )

@dashboard_bp.route('/add_transaction', methods=['POST'])
@login_required
def add_transaction():
    accounts = Account.query.filter_by(user_id=current_user.id).all()
    categories = Category.query.filter_by(user_id=current_user.id).all()
    form = TransactionForm()
    form.account_id.choices = [(a.id, a.name) for a in accounts] + [(-1, "+ Add another account")]
    tx_type = request.form.get('type')
    if tx_type == 'income':
        form.category.choices = [(c.name, c.name) for c in categories if c.type == 'income'] + [("add_category", "+ Add new category")]
    else:
        form.category.choices = [(c.name, c.name) for c in categories if c.type == 'expense'] + [("add_category", "+ Add new category")]

    if form.validate_on_submit():
        new_tx = Transaction(
            user_id=current_user.id,
            account_id=form.account_id.data,
            amount=form.amount.data,
            category=form.category.data,
            type=tx_type,
            date=form.date.data,
            description=form.description.data
        )
        db.session.add(new_tx)
        db.session.commit()
        flash(f"{tx_type.capitalize()} added successfully.", "success")
    else:
        flash("Please correct the errors in the form.", "danger")
    return redirect(url_for('dashboard.dashboard'))

@dashboard_bp.route('/add_category', methods=['POST'])
@login_required
def add_category():
    name = request.form.get('category_name')
    cat_type = request.form.get('category_type')
    if name and cat_type in ['income', 'expense']:
        exists = Category.query.filter_by(user_id=current_user.id, name=name, type=cat_type).first()
        if not exists:
            cat = Category(name=name, type=cat_type, user_id=current_user.id)
            db.session.add(cat)
            db.session.commit()
            return jsonify(success=True)
        else:
            return jsonify(success=False, message="Category already exists.")
    return jsonify(success=False, message="Invalid data.")

@dashboard_bp.route('/add_account', methods=['POST'])
@login_required
def add_account():
    name = request.form.get('account_name')
    if name:
        exists = Account.query.filter_by(user_id=current_user.id, name=name).first()
        if not exists:
            acc = Account(name=name, user_id=current_user.id)
            db.session.add(acc)
            db.session.commit()
            return jsonify(success=True)
        else:
            return jsonify(success=False, message="Account already exists.")
    return jsonify(success=False, message="No account name provided.")

@dashboard_bp.route('/delete_transaction/<int:tx_id>', methods=['POST'])
@login_required
def delete_transaction(tx_id):
    tx = Transaction.query.filter_by(id=tx_id, user_id=current_user.id).first()
    if tx:
        db.session.delete(tx)
        db.session.commit()
        flash("Transaction deleted.", "success")
    else:
        flash("Transaction not found.", "danger")
    return redirect(url_for('dashboard.dashboard'))