from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SelectField, SubmitField, TextAreaField, DateField
from wtforms.validators import DataRequired, NumberRange, Length, Optional
from datetime import date

class TransactionForm(FlaskForm):
    """
    A unified form for adding both income and expense transactions.
    """
    type = SelectField(
        'Type',
        choices=[('income', 'Add Money'), ('expense', 'Add Expense')],
        validators=[DataRequired()],
    )

    amount = DecimalField(
        'Amount (Rs)',
        validators=[
            DataRequired(),
            NumberRange(min=0.01, message="Amount must be greater than zero.")
        ]
    )

    category = SelectField(
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
        ],
        validators=[DataRequired()]
    )

    description = TextAreaField(
        'Description (optional)',
        validators=[Optional(), Length(max=200, message='Description cannot exceed 200 characters.')]
    )

    date = DateField(
        'Date',
        format='%Y-%m-%d',
        default=date.today,
        validators=[DataRequired()]
    )

    # If you want to support selecting an account in the transaction modal:
    account_id = SelectField(
        'Account',
        coerce=int,
        validators=[DataRequired()],
        choices=[]  # You should set choices in your route before rendering the form
    )

    submit = SubmitField('Submit Transaction')

class CreateAccountForm(FlaskForm):
    name = StringField('Account Name', validators=[DataRequired(), Length(min=2, max=50)])
    submit = SubmitField('Create Account')