from flask import Flask 
from config import Config
from flask_sqlachemy import SQLAlchemy
from flask_migrate import Migrate


flask_app = Flask(__name__)
flask_app.config.from_object(Config)
database = SQLAlchemy(flask_app)
migrate = Migrate(app, db)

from app import routes, models
