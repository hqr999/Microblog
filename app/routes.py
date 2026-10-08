from flask import render_template, flash, redirect, url_for
from app import flask_app
from app.forms import LoginForm


@flask_app.route("/")
@flask_app.route("/index")
def index():
    user = {"username": "Henrique"}
    posts = [
        {"author": {"username": "John"}, "body": "Dia lindo em Portland"},
        {"author": {"username": "Susan"}, "body": "Os filmes dos Vingadores são tão legais!!"},
    ]

    return render_template("index.html", title="Home", user=user, posts=posts)
    # return render_template('index.html',user=user)


@flask_app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(
            "Login requisitado pelo usuário {}, me-lembre {}".format(
                form.username.data, form.remember_me.data
            )
        )
        return redirect(url_for('index'))
    return render_template("login.html", title="Se Inscreva", form=form)
