from flask import render_template
from app import flask_app
from app.forms import LoginForm

@flask_app.route("/")
@flask_app.route("/index")
def index():
    user = {"username": "Henrique"}
    posts = [
        {"author": {"username": "John"}, "body": "Beautiful day in Portland"},
        {"author": {"username": "Susan"}, "body": "The Avengers movies was so cool!"},
    ]

    return render_template("index.html", title="Home", user=user,posts=posts)
    # return render_template('index.html',user=user)



@flask_app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html',title="Se Inscreva", form=form)
