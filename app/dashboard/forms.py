# app/dashboard/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SelectField, SubmitField, TextAreaField # Added TextAreaField
from wtforms.validators import DataRequired, NumberRange, Length, Optional

class TransactionForm(FlaskForm):
    """
    A unified form for adding both income and expense transactions.
    """
    type = SelectField(
        'Type',
        choices=[('income', 'Add Money'), ('expense', 'Add Expense')],
        validators=[DataRequired()],
        # Optional: You might want to set a default or use client-side JS to pre-select
        # based on which button (Add Money/Add Expense) was clicked.
    )

    amount = DecimalField(
        'Amount (Rs)',
        validators=[
            DataRequired(),
            NumberRange(min=0.01, message="Amount must be greater than zero.")
        ]
    )

    category = SelectField( # Changed from StringField to SelectField as per your request
        'Category',
        choices=[
            ('salary', 'Salary'),
            ('business', 'Business'),
            ('freelance', 'Freelance'),
            ('food', 'Food'),
            ('transport', 'Transport'),
            ('entertainment', 'Entertainment'),
            ('shopping', 'Shopping'),
            ('bills', 'Bills'),
            ('misc', 'Miscellaneous'),
            # You might want to add more categories or allow users to define custom ones
        ],
        validators=[DataRequired()]
    )

    description = TextAreaField( # Changed from StringField to TextAreaField
        'Description (optional)',
        validators=[Optional(), Length(max=200, message='Description cannot exceed 200 characters.')]
    )

    submit = SubmitField('Submit Transaction') # Generic submit button text
