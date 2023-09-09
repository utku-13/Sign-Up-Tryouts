from flask import Flask, render_template, request, flash, redirect, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from form import SignUpForm, SignInFormForm
from flask_bootstrap import Bootstrap
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from functools import wraps
import os

app = Flask(__name__)
Bootstrap(app)
# To activate wtf forms we did above!

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQALCHEMY_TRACK_MODIFICATIONS"] = False 

app.config['SECRET_KEY']='123456'
#this is for forms!

db = SQLAlchemy(app)

class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=False)
    email = db.Column(db.String(250), unique=True)
    password = db.Column(db.String, nullable=False)

with app.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"#login fonksiyonu isminden geliyo dene yine de!

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@app.route('/')
def home():
    return render_template('entry.html')

@app.route('/register',methods=['GET','POST'])
def register():
    form=SignUpForm()
    if form.validate_on_submit():
        new_user = Users(name=form.name.data,
                         email=form.email.data,
                         password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('index.html', form_name='Register Form', form=form)

@app.route('/sign-in',methods=["GET","POST"])
def sign_in():
    form=SignInFormForm()
    if form.validate_on_submit():
        try: 
            user = db.session.query(Users).filter_by(email=form.email.data).scalar()
            if user.password == form.password.data :
                login_user(user)
                print("User Succesfully logged in!")
            return redirect(url_for('home'))
        except:
            flash("This email has not registered yet!",'error')
    return render_template('index.html',form_name="Sign In",form=form)

@app.route('/log-out')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

def only_admin(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        print(current_user.id)
        if current_user.id != 1 :
            return abort(403)
        else:
            return f(*args,**kwargs)
    return decorated_function
#last row dont really have a meaning because it will eventually return 
# oen of those above so it is just thing.

@app.route('/post-page',methods=['GET','POST'])
@only_admin
def post():
    return render_template('post.html')



if __name__ == "__main__":
    app.run(debug=True)