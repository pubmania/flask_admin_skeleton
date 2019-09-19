# flask_admin_skeleton
This app shows the basic usage of Flask framework. It allows creation and deletion of users.   
A user can self register but will require and approval from administrator before the user can have access to database entries.

Once the user has access, (s)he can create a post and enter expenses. This functionality demonstrates the usage of `wtforms`.
More specifically, usage of dropdown and display of date field and checkboxes.

Further activities to explore:
* Create a grid editable form
* Creation of subforms
* Modals
  * ~~Creation and submission of forms using Modals.~~ - Works
  * Validation to display in Modals and not take back to the page form. - Pending.

# Demo
A working demo is available on the link: https://flask-admin-skeleton.herokuapp.com

or deploy your own:

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

# How To?

1. Clone this repository on your desktop in the python virtual environment.
2. Run following commands to install dependencies:
```python
pip install --upgrade pip
pip install gunicorn flask run.py flask-bootstrap flask-mail flask-SQLAlchemy flask-bcrypt flask-table flask-wtf flask-login pillow
```
3. Go to the directory `approot` on terminal / commandline and give the command `python run.py`
4. Although step 2 should have taken care of all dependencies, install any missing dependencies depending on any error during the startup.
5. Once the run.py has worked, press `Ctrl+C` to stop the server.
6. Then type python and in the python interpreter initiate database using the `create_admin_user.py`
7. Now start the app by typing `python run.py`
8. In your browser type: http://localhost:5000/ and register a user with your own username and password.
9. Login using the username `admin@admin.com` and password `adminpassword`
10. Go to "Registered Users" link and update the user role to `Admin`.
11. Logout and login with user you created in Step 7.
12. Go to Registered users and delete the default admin user you created.
13. Explore further!!!
