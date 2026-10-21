from flask import render_template, flash, redirect, url_for, request
from app import flask_app, database
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa 
from app.models import User
from urllib.parse import urlsplit 


@flask_app.route("/")
@flask_app.route("/index")
@login_required
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
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = database.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Senha ou Nome de Usuário inválido')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html',title='ENtre', form=form)



@flask_app.route('/logout')
def logout():
    logout_user() 
    return redirect(url_for('index'))
