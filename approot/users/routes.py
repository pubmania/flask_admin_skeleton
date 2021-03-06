from flask import render_template, url_for, flash, redirect, request, Blueprint, abort, jsonify, json
from flask_login import login_user, current_user, logout_user, login_required
from approot import db, bcrypt
from approot.models import User, Post, Expense
from approot.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm, UpdateRegistredUsersForm)
from approot.expenses.forms import ExpenseForm
from approot.users.utils import save_picture, send_reset_email
import approot.main.utils
from approot.main.utils import get_symbol

users = Blueprint('users', __name__)

##########################  New Change to allow usage of just one template for tabular views#######################
@users.route("/registeredusers", methods=['GET', 'POST'])
@login_required
def registeredusers():
    if current_user.role != 'Admin':
        flash('Your role does not permit access to this page!', 'danger')
        abort(403)
    form = UpdateRegistredUsersForm()
    displayfields = ['author', 'email', 'role', 'dark_mode_get_symbol', 'theme']
    editfields = [
    {'name':'username'},
    {'name':'email'},
    {'name':'role'},
    {'name':'dark_mode','switch':True},
    {'name':'theme'}
    ]
    columns = [
    {'name':'Username','sortable':"true"},
    {'name':'Email','sortable':"false"},
    {'name':'Role','sortable':"true"},
    {'name':'Dark Mode','sortable':"false"},
    {'name':'Theme','sortable':"false"}]
    rows = []
    users = User.query.order_by(User.username.desc()).all()
    for user in users:
        userdict = {'id':user.id,
        'author':user.username,
        'email':user.email,
        'role':user.role,
        'dark_mode_get_symbol':get_symbol(user.dark_mode),
        'dark_mode':user.dark_mode,
        'username':user.username,
        'theme':user.theme}
        rows.append(userdict)
    row_id=None
    return render_template('tabular_view.html', form=form, \
    columns=columns, rows=rows, fields=displayfields, editfields=editfields, \
    update_route='users.update_user', self_route='users.registeredusers',row_id=row_id, \
    delete_route='users.delete_user', title='Registerd Users')

@users.route("/user/update/<int:row_id>", methods=['GET', 'POST'])
@login_required
def update_user(row_id):
    user = User.query.get_or_404(row_id)

    form = UpdateRegistredUsersForm()
    if form.validate_on_submit():
        try:
            user.username = form.username.data
            user.email = form.email.data
            user.role = form.role.data
            user.dark_mode = form.dark_mode.data
            user.theme = form.theme.data
            db.session.commit()
            flash('User details have been updated!', 'success')
            return redirect(url_for('users.registeredusers'))
        except Exception as e:
            db.session.rollback()
            s = str(e)
            if "user.username" in s:
                flash('This username is already taken. Please chose a different one.', 'danger')
                flash('User details have not been updated', 'warning')
            elif "user.email" in s:
                flash('This email is already registered. Please chose a different one.', 'danger')
                flash('User details have not been updated', 'warning')
            else:
                flash(s, 'warning')
    return redirect(url_for('users.registeredusers', row_id=row_id))

@users.route("/user/delete/<int:row_id>", methods=['POST'])
@login_required
def delete_user(row_id):
    user = User.query.get_or_404(row_id)
    if user.id == current_user.id:
        flash('You cannot delete your own account!', 'danger')
        abort(403)
    db.session.delete(user)
    db.session.commit()
    flash('User has been deleted!', 'success')
    return redirect(url_for('users.registeredusers'))


###################################################################################################################

@users.route("/registeredtestuser", methods=['GET', 'POST'])
@login_required
def registeredtestuser():
    #page = request.args.get('page', 1, type=int)
    #users = User.query.order_by(User.username.desc()).paginate(page=page, per_page=5)
    users = User.query.order_by(User.username.desc()).all()
    form = UpdateRegistredUsersForm()
    users_data = User.query.order_by(User.username.desc()).all()
    return render_template('user/unused_registeredusers.html', title='Registered Users', form=form, users=users)

@users.route("/testuser/delete/<int:user_id>", methods=['POST'])
@login_required
def delete_testuser(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('You cannot delete your own account!', 'danger')
        abort(403)
    db.session.delete(user)
    db.session.commit()
    flash('User has been deleted!', 'success')
    return redirect(url_for('users.registeredtestusers'))

@users.route("/testuser/update/<int:user_id>", methods=['GET', 'POST'])
@login_required
def update_testuser(user_id):
    user = User.query.get_or_404(user_id)
    #if user.id == current_user.id:
    #    flash('You cannot update your own account!', 'danger')
    #    abort(403)
    form = UpdateRegistredUsersForm()
    if form.validate_on_submit():
        try:
            user.username = form.username.data
            user.email = form.email.data
            user.role = form.role.data
            db.session.commit()
            flash('User details have been updated!', 'success')
            return redirect(url_for('users.registeredtestusers'))
        except Exception as e:
            db.session.rollback()
            s = str(e)
            if "user.username" in s:
                flash('This username is already taken. Please chose a different one.', 'danger')
                flash('User details have not been updated', 'warning')
            elif "user.email" in s:
                flash('This email is already registered. Please chose a different one.', 'danger')
                flash('User details have not been updated', 'warning')
            else:
                flash(s, 'warning')
    return redirect(url_for('users.registeretestdusers', user_id=user_id))


@users.route("/register", methods=['GET', 'POST'])
#@login_required
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, role="Pending")
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('user/register_wtf.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('user/login.html', title='Login', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.about'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.dark_mode = form.dark_mode.data
        current_user.theme = form.theme.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.dark_mode.data = current_user.dark_mode
        form.theme.data = current_user.theme
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('user/account.html', title='Account',
                           image_file=image_file, form=form)


@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('post/user_posts.html', posts=posts, user=user)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('user/reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('user/reset_token.html', title='Reset Password', form=form)
