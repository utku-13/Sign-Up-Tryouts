from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///all_users.db"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=False)
    email = db.Column(db.String(250), unique=True)
    password = db.Column(db.String, nullable=False)

with app.app_context():
    db.create_all()

#I COMMENTED BELOW BECAUSE IT IS MANUAL WAY TO ADD ELEMET
#TO DATABASE WE WILL AUTOMATE THIS AND CONNECT TO WTFFORMS.

# with app.app_context():
#     new_user = User(name="utku",email='ozerutku13@gmail.com',password="U147613d")
#     db.session.add(new_user)
#     db.session.commit()

with app.app_context():
    all_books = db.session.query(User).filter_by(name="utku").scalar()
    print(all_books.password)