"""Creates instance of Flask app"""
from flask import Flask
from blueprints import setup
from blueprints import blog

def create_app():
    """Creates app"""
    app=Flask(__name__, template_folder='templates')
    app.config.from_mapping(
        SECRET_KEY="secret",
        DB_TYPE = "db")
    app.app_context().push()
    app.register_blueprint(setup.bp)
    app.register_blueprint(blog.bp)
    return app
