from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from approot import db
from approot.models import Expense, User
from approot.expenses.forms import ExpenseForm

expenses = Blueprint('expenses', __name__)

@expenses.route("/expense")
@login_required
def expense():
    #page = request.args.get('page', 1, type=int)
    #expenses = Expense.query.order_by(Expense.expense_date.desc()).paginate(page=page, per_page=5)
    expenses = Expense.query.order_by(Expense.expense_date.desc()).all()
    form = ExpenseForm()
        #return redirect(url_for('expenses.expense'))
    return render_template('expense/expense.html', expenses=expenses, form=form)

@expenses.route("/user/expenses/<string:username>")
def user_expenses(username):
    #page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    form = ExpenseForm()
    expenses = Expense.query.filter_by(author=user)\
        .order_by(Expense.expense_date.desc())\
        .all()
        #.paginate(page=page, per_page=5)
    return render_template('expense/expense.html', expenses=expenses, user=user, form=form)

@expenses.route("/expense/new", methods=['GET', 'POST'])
@login_required
def new_expense():
    page = request.args.get('page', 1, type=int)
    expenses_from_query = Expense.query.order_by(Expense.expense_date.desc()).paginate(page=page, per_page=5)
    form = ExpenseForm()
    if form.validate_on_submit():
        expense = Expense(description=form.description.data, expense_date=form.expense_date.data,
                        amount=form.amount.data,vat_amount=form.vat_amount.data,Transferrable=form.Transferrable.data, author=current_user)
        db.session.add(expense)
        db.session.commit()
        flash('Your expense has been created!', 'success')
        return redirect(url_for('expenses.expense'))
    #return render_template('expense/unused_create_expense.html', title='New Expense',
    #                       form=form, legend='New Expense')
    return render_template('expense/expense.html', expenses=expenses_from_query, form=form)


@expenses.route("/expense/update/<int:expense_id>", methods=['GET', 'POST'])
@login_required
def update_expense(expense_id):
    #page = request.args.get('page', 1, type=int)
    #expenses_from_query = Expense.query.order_by(Expense.expense_date.desc()).paginate(page=page, per_page=5)
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
        return redirect(url_for('expenses.expense'))
        """ Commented to see if this will have any negative effect on the flow - I think it won't
    elif request.method == 'GET':
        form.description.data = expense.description
        form.amount.data = expense.amount
        form.expense_date.data = expense.expense_date
        form.vat_amount.data = expense.vat_amount
        form.Transferrable.data = expense.Transferrable """
    #return render_template('expense/expense.html', title='Update Expense',
    #                       form=form, legend='Update Expense')
    #return render_template('expense/expense.html', expenses=expenses_from_query, form=form, expense_id=expense_id)
    return redirect(url_for('expenses.expense'), expense_id=expense_id)

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
