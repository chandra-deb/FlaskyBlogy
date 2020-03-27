from flask import  render_template, flash, redirect, url_for
from app import  app
from app.forms import  LoginForm, RegistrationForm
from flask_login import current_user, login_user
from app.models import  User
from werkzeug.security import check_password_hash


@app.route('/')
@app.route('/index')
def index():
    
    user = {
        'username' : 'Chandra'
        }
    posts = [
        {
        'author':{'username':'Jonn Lin'},
        'body':'A beautiful day in Bangladesh'
    },
    {
        'author':{'username':'Suvro Barman'},
        'body':'The Marvel Avengers!'
    }
    ]
    return render_template('index.html', user=user, title='Home', posts=posts)



@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not check_password_hash(user.hashed_password, form.password.data):
            flash('Invalid information!')
            return redirect(url_for('login'))
        login_user(user, form.remember_me.data)
        flash('Login Successful!', category='success')
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    return render_template('register.html', title='Sign Up', form=form)