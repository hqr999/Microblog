import sqlalchemy as sa
import sqlalchemy.orm as so
from app import flask_app, database
from app.models import User, Post


@flask_app.shell_context_processor
def make_shell_context():
    return {
            'sa':sa,
            'so':so,
            'database':database,
            'User': User, 
            'Post': Post
    }
