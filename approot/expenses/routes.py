from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint, json)
from flask_login import current_user, login_required
from approot import db
from approot.models import Expense, User
from approot.expenses.forms import ExpenseForm
from approot.main.utils import get_symbol
expenses = Blueprint('expenses', __name__)

########################## New Change to allow usage of just one template for tabular views###############
@expenses.route("/expense", defaults={'continue_flag': 'No'}, methods=['GET', 'POST'])
@expenses.route("/expense/<string:continue_flag>", methods=['GET', 'POST'])
@login_required
def expense(continue_flag):
    #expenses = Expense.query.filter_by(author=current_user).order_by(Expense.expense_date.desc()).all()
    form = ExpenseForm()

    displayfields = ['author', 'description', 'amount', 'expense_date', 'vat_amount', 'Transferrable_val']
    editfields = [
    {'name':'description'},
    {'name':'amount'},
    {'name':'expense_date'},
    {'name':'vat_amount'},
    {'name':'Transferrable', 'switch':False}
    ]

    buttonName = 'Add New Expenses'
    columns = [
    {'name':'Author','sortable':"true"},
    {'name':'Description','sortable':"true"},
    {'name':'Amount','sortable':"true"},
    {'name':'Expense Date','sortable':"true"},
    {'name':'VAT Amount','sortable':"false"},
    {'name':'Transferrable','sortable':"false"}]
    rows = []
    expenses = Expense.query.order_by(Expense.expense_date.desc()).all()
    for expense in expenses:

        #if expense.Transferrable == True:
        #    transferrable_var = u'\u2714'
        #else:
        #    transferrable_var = u'\u2717'
        expensedict = {'id':expense.id, 'author':expense.author.username,
                      'description':expense.description, 'amount':"{:.2f}".format(expense.amount),
                      'expense_date':expense.expense_date.strftime('%Y-%m-%d'),
                      'vat_amount':"{:.2f}".format(expense.vat_amount), 'Transferrable_val':get_symbol(expense.Transferrable),
                      'Transferrable':expense.Transferrable
                      }
        rows.append(expensedict)

    return render_template('tabular_view.html', form=form, columns=columns, rows=rows, \
    fields=displayfields, editfields=editfields, update_route='expenses.update_expense', \
    self_route='expenses.expense', create_route='expenses.new_expense', buttonName=buttonName,\
    delete_route='expenses.delete_expense', continue_flag=continue_flag)

@expenses.route("/expense/new/<string:continue_flag>", methods=['GET','POST'])
@login_required
def new_expense(continue_flag):
    form = ExpenseForm()
    if form.validate_on_submit():
        expense = Expense(description=form.description.data, expense_date=form.expense_date.data,
                        amount=form.amount.data,vat_amount=form.vat_amount.data,Transferrable=form.Transferrable.data, author=current_user)
        db.session.add(expense)
        db.session.commit()
        flash('Your expense has been created!', 'success')
    return redirect(url_for('expenses.expense',continue_flag=continue_flag))


@expenses.route("/expense/update/<int:row_id>", methods=['GET', 'POST'])
@login_required
def update_expense(row_id):
    expense = Expense.query.get_or_404(row_id)
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
    return redirect(url_for('expenses.expense', row_id=row_id))

@expenses.route("/expense/delete/<int:row_id>", methods=['POST'])
@login_required
def delete_expense(row_id):
    expense = Expense.query.get_or_404(row_id)
    if expense.author != current_user:
        abort(403)
    db.session.delete(expense)
    db.session.commit()
    flash('Your expense has been deleted!', 'success')
    return redirect(url_for('expenses.expense'))
##########################################################################################################

@expenses.route("/testexpense")
@login_required
def testexpense():
    #page = request.args.get('page', 1, type=int)
    #expenses = Expense.query.order_by(Expense.expense_date.desc()).paginate(page=page, per_page=5)
    expenses = Expense.query.order_by(Expense.expense_date.desc()).all()
    form = ExpenseForm()
        #return redirect(url_for('expenses.expense'))
    return render_template('expense/expense.html', expenses=expenses, form=form)

@expenses.route("/testexpense/new", methods=['POST'])
@login_required
def new_testexpense():
    form = ExpenseForm()
    if form.validate_on_submit():
        expense = Expense(description=form.description.data, expense_date=form.expense_date.data,
                        amount=form.amount.data,vat_amount=form.vat_amount.data,Transferrable=form.Transferrable.data, author=current_user)
        db.session.add(expense)
        db.session.commit()
        flash('Your expense has been created!', 'success')
    return redirect(url_for('expenses.testexpense'))

@expenses.route("/user/testexpenses/<string:username>")
def user_testexpenses(username):
    #page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    form = ExpenseForm()
    expenses = Expense.query.filter_by(author=user)\
        .order_by(Expense.expense_date.desc())\
        .all()
        #.paginate(page=page, per_page=5)
    return render_template('expense/testexpense.html', expenses=expenses, user=user, form=form)

@expenses.route("/testexpense/update/<int:expense_id>", methods=['GET', 'POST'])
@login_required
def update_testexpense(expense_id):
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
    return redirect(url_for('expenses.testexpense', expense_id=expense_id))

@expenses.route("/testexpense/delete/<int:expense_id>", methods=['POST'])
@login_required
def delete_testexpense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    if expense.author != current_user:
        abort(403)
    db.session.delete(expense)
    db.session.commit()
    flash('Your expense has been deleted!', 'success')
    return redirect(url_for('expenses.testexpense'))
