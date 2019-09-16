from flask import render_template, request, Blueprint
from approot.models import Expense
from approot.expenses.forms import ExpenseForm
from flask_login import current_user, login_required

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    expenses = Expense.query.order_by(Expense.expense_date.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', expenses=expenses)


@main.route("/about")
def about():
    page = request.args.get('page', 1, type=int)
    expenses = Expense.query.order_by(Expense.expense_date.desc()).paginate(page=page, per_page=5)
    return render_template('about.html', expenses=expenses)
