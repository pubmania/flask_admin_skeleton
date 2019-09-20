
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField, BooleanField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired
from flask_table import Table, Col, LinkCol


class ExpenseForm(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    expense_date = DateField('Expense Date',format='%Y-%m-%d', validators=[DataRequired()])
    amount = DecimalField('Amount',places=2, validators=[DataRequired()])
    vat_amount = DecimalField('VAT Amount',places=2)
    Transferrable = BooleanField('Transferrable?')
    submit = SubmitField('Submit')
