from flask import  render_template, flash, redirect, url_for, request
from app import  app, db
from app.forms import  LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import  User
from werkzeug.security import check_password_hash


@app.route('/')
@app.route('/index')
@login_required
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
    return render_template('index.html', title='Home', posts=posts)



@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not check_password_hash(user.password_hash, form.password.data):
            flash('Invalid information!')
            return redirect(url_for('login'))
        login_user(user, form.remember_me.data)
        flash('Login Successful!', category='success')
        next_page = request.args.get('next')
        if not next_page:
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)



@app.route('/logout')
def logout():
    if current_user.is_anonymous:
        flash("You are already logged out.")
        return redirect(url_for('index'))
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.confirm_password.data)
        db.session.add(user)
        db.session.commit()
        flash('You are now a registred user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Sign Up', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, title=user.username, posts=posts)