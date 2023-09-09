from flask import Flask,render_template
from form import SignUpForm
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'
Bootstrap(app)

@app.route('/',methods=['GET','POST'])
def home():
    form = SignUpForm()
    if form.validate_on_submit():
        print(f"{form.name.data,form.email.data,form.password.data}")
    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)