from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length 
import sqlalchemy as sa 
from app import database 
from app.models import User



class LoginForm(FlaskForm):
    username = StringField('Nome de Usuário',validators=[DataRequired()])
    password = StringField('Senha',validators=[DataRequired()])
    remember_me = BooleanField('Lembre-me')
    submit = SubmitField('Entrar')


class RegistrationForm(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    pwd = PasswordField('Senha', validators=[DataRequired()])
    pwd2 = PasswordField('Repita a Senha', validators=[DataRequired(), EqualTo('pwd')])
    submit = SubmitField('Registrar')


    def validate_username(self, username):
        user = database.session.scalar(sa.select(User).where(User.username == username.data))
        if user is not None:
            raise ValidationError('Por favor use um nome de usuário diferente.')


    def validate_email(self, email):
        user = database.session.scalar(sa.select(User).where(User.email == email.data))
        if user is not None:
            raise ValidationError('Por Favor use um endereço de email diferente.')




class EditorProfileForm(FlaskForm):
    username = StringField('Nome de Usuário',validators=[DataRequired()])
    about_me = TextAreaField('Sobre mim',validators=[Length(min=0,max=140)])
    submit = SubmitField('Submit')
