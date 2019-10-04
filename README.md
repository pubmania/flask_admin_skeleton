# flask_admin_skeleton

This app shows the basic usage of Flask framework. It allows creation and deletion of users.   
A user can self register but will require an approval from administrator before the user can have access to database entries.

Once the user has access, (s)he can create a post and enter expenses. This functionality demonstrates the usage of `wtforms`.
More specifically, usage of dropdown and display of date field and checkboxes.

# Change Log:
04/10/2019
* Added dark and light mode switch
* Added the ability for user to change available themes
* Change Account Page to have groupings for settings and user info.

01/10/2019
* Updated Macro to make it work better for SelectField (populate the selected option on update form), DecimalField (add number fieldtype and step)
* Created tabular_view.html which can be used for displaying table for any query data. All data to be displayed and columns can just be passed from routes.py.
* Complete rewrite of expenses and users routes to make them work with single template - Ensuring DRY principle.
* Added "Save and Continue" functionality on the "AddModal"

22/09/2019
* Bootstrap Table related - Removed Server side pagination
* Moved User Expense from User blue print to Expense Blue Print
* Changed landing page to about.html and made home page accessible to logged in users.
* Created a dark theme and applied as default.


# Further activities to explore:

* ~~Create Macro for creating fields~~ - Done
* ~~Create a grid editable form~~ - Added following functionality on expenses page:
  * ~~Ability to make a row editable using edit button.~~ - Done (For Expense Page)
  * ~~Ability to update using Modal Form.~~ - Done (For User Page)
  * ~~Add "search" box. - Basic Search on expenses table is added but can be improved.~~ Done - Applied [Bootstrap Table](https://bootstrap-table.com/)
  * Add "select" row and "multiple delete" - Explore "bootstrap table" as an option.

* Modals
  * ~~Creation and submission of forms using Modals.~~ - Done
  * ~~Validation to display in Modals and not take back to the page form.~~ - Done
  * ~~Make the update button disappear for entries created by other users.~~ Done
  * ~~Make modal changes for Users table~~ Done
  * Make modal changes for Posts Table.
  * Clean Up code
* Creation of subforms - Possibly just a mechanism to add modals. ~~Although need to understand the cascade of deletion using SQLAlchemy.~~ CASCADE Deletion now works. Just needed to ensure the models definition included `cascade='all,delete,delete-orphan'` in the relationship definition.

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
3. Go to the directory `approot` on terminal / commandline and type the command `python run.py`
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
