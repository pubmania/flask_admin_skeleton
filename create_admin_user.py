from approot import create_app, db, bcrypt
from approot.models import User, Post, Expense
app = create_app()

db.app = app
db.drop_all()
db.create_all()

user=User()

user.username = 'admin'
user.email = 'admin@admin.com'
user.role = 'Admin'
hashed_password = bcrypt.generate_password_hash("adminpassword").decode('utf-8')

user.password = hashed_password

db.session.add(user)
db.session.commit()
