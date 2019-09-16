from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from approot import db
from approot.models import Expense
from approot.expenses.forms import ExpenseForm

expenses = Blueprint('expenses', __name__)


@expenses.route("/expense/new", methods=['GET', 'POST'])
@login_required
def new_expense():
    form = ExpenseForm()
    if form.validate_on_submit():
        expense = Expense(description=form.description.data, expense_date=form.expense_date.data,
                        amount=form.amount.data,vat_amount=form.vat_amount.data,Transferrable=form.Transferrable.data, author=current_user)
        db.session.add(expense)
        db.session.commit()
        flash('Your expense has been created!', 'success')
        return redirect(url_for('expenses.expense'))
    return render_template('expense/create_expense.html', title='New Expense',
                           form=form, legend='New Expense')


@expenses.route("/expense")
@login_required
def expense():
    page = request.args.get('page', 1, type=int)
    expenses = Expense.query.order_by(Expense.expense_date.desc()).paginate(page=page, per_page=5)
    form = ExpenseForm()
    return render_template('expense/expense.html', expenses=expenses, form=form)


@expenses.route("/expense/update/<int:expense_id>", methods=['GET', 'POST'])
@login_required
def update_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    if expense.author != current_user:
        abort(403)
    form = ExpenseForm()
    if form.validate_on_submit():
        expense.description = form.description.data
        expense.amount = form.amount.data
        expense.expense_date = form.expense_date.data
        expense.vat_amount = form.vat_amount.data
        expense.Transferrable = form.Transferrable.data
        db.session.commit()
        flash('Your expense has been updated!', 'success')
        return redirect(url_for('expenses.expense', expense_id=expense.id))
    elif request.method == 'GET':
        form.description.data = expense.description
        form.amount.data = expense.amount
        form.expense_date.data = expense.expense_date
        form.vat_amount.data = expense.vat_amount
        form.Transferrable.data = expense.Transferrable
    return render_template('expense/create_expense.html', title='Update Expense',
                           form=form, legend='Update Expense')


@expenses.route("/expense/delete/<int:expense_id>", methods=['POST'])
@login_required
def delete_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    if expense.author != current_user:
        abort(403)
    db.session.delete(expense)
    db.session.commit()
    flash('Your expense has been deleted!', 'success')
    return redirect(url_for('expenses.expense'))