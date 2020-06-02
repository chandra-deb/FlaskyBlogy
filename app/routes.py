from app import app, db
from flask import render_template, redirect, flash, url_for, request
from app.forms import LoginForm, RegistrationForm
from flask_login import login_user, logout_user, current_user, login_required
from app.models import User, check_password_hash



@app.route('/')
@app.route('/home')
@login_required
def home():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', posts=posts, title="Home")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Something is incorrect. Please try again!')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page:
            next_page = url_for('home')
        return redirect(next_page) 
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
   logout_user()
   return redirect(url_for('login'))     


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!')
        
        return redirect(url_for('login'))
    return render_template('register.html', form=form, title='Sign Up')