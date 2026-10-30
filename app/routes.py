from flask import render_template, flash, redirect, url_for, request
from app import flask_app, database
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa 
from app.models import User
from urllib.parse import urlsplit 
from datetime import datetime, timezone
from app.forms import EditorProfileForm


@flask_app.route("/")
@flask_app.route("/index")
@login_required
def index():
    user = {"username": "Henrique"}
    posts = [
        {"author": {"username": "John"}, "body": "Dia lindo em Portland"},
        {"author": {"username": "Susan"}, "body": "Os filmes dos Vingadores são tão legais!!"},
    ]

    return render_template("index.html", title="Página Inicial", posts=posts)


@flask_app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = database.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_pwd(form.password.data):
            flash('Senha ou Nome de Usuário inválido')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html',title='Entre', form=form)



@flask_app.route('/logout')
def logout():
    logout_user() 
    return redirect(url_for('index'))



@flask_app.route('/registrar', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_pwd(form.pwd.data)
        database.session.add(user)
        database.session.commit()
        flash('Parabéns, você registrou um novo usuário!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Registrar',form=form)



@flask_app.route('/usuario/<username>')
@login_required
def user(username):
    user = database.first_or_404(sa.select(User).where(User.username == username))
    posts = [
            {'author': user, 'body': 'Teste post #1'},
            {'author': user, 'body': 'Teste post #2'}
    ]

    return render_template('user.html',user=user,posts=posts)




@flask_app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        database.session.commit()


@flask_app.route('/editar_perfil', methods=['GET','POST'])
@login_required
def edit_profile():
    form = EditorProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        database.session.commit()
        flash('Suas mudanças foram salvas')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me

    return render_template('edit_profile.html', title='Editar Perfil',form=form)
