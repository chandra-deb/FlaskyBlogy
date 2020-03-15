from flask import  render_template, flash, redirect, url_for
from app import  app
from app.forms import  LoginForm, RegistrationForm


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
    form = LoginForm()
    if form.validate_on_submit():

        if form.username.data == 'Chandra' and form.password.data == 'password':
            flash('Login Successful!',category='success')
            return redirect(url_for('index'))

    return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    return render_template('register.html', title='Sign Up', form=form)