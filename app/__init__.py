from flask import Flask 
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging 
from logging.handlers import SMTPHandler


flask_app = Flask(__name__)
flask_app.config.from_object(Config)
database = SQLAlchemy(flask_app)
migrate = Migrate(flask_app, database)
login = LoginManager(flask_app)
login.login_view = 'login'


if not flask_app.debug:
    if flask_app.config['MAIL_SERVER']:
        auth = None
        if flask_app.config['MAIL_USERNAME'] or flask_app.config['MAIL_PASSWORD']:
            auth = (flask_app.config['MAIL_USERNAME'], flask_app.config['MAIL_PASSWORD'])
        secure = None
        if flask_app.config['MAIL_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(flask_app.config['MAIL_SERVER'], flask_app.config['MAIL_PORT']),
            fromaddr='no-reply@' + flask_app.config['MAIL_SERVER'],
            toaddrs=flask_app.config['ADMINS'],
            subject='Falha no Microblog',
            credentials=auth,
            secure=secure,
        )
        mail_handler.setLevel(logging.ERROR)
        flask_app.logger.addHandler(mail_handler)


from app import routes, models, errors
