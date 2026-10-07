from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired



class LoginForm(FlaskForm):
    username = StringField('Nome de Usuário',validators=[DataRequired()])
    password = StringField('Senha',validators=[DataRequired()])
    remember_me = BooleanField('Lembre-me')
    submit = SubmitField('Se inscrever')
