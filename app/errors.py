from flask import render_template
from app import flask_app, database


@flask_app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@flask_app.errorhandler(500)
def internal_error(error):
    database.session.rollback()
    return render_template('500.html'), 500
