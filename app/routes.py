from flask import  render_template
from app import  app


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