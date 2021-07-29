"""Creates instance of Flask app"""
from flask import Flask, session
from models.user import User
from blueprints import setup
from blueprints import users
from blueprints import blog
from blueprints import auth
from database.database import Database

def create_app():
    """Creates app"""
    app=Flask(__name__, template_folder='templates')
    app.config.from_mapping(
        SECRET_KEY="secret",
        DB_TYPE = "memory")
    app.app_context().push()
    
    @app.before_first_request
    def create_tables():
        Database().create_update_tables()

    app.register_blueprint(setup.bp)
    app.register_blueprint(users.bp)
    app.register_blueprint(blog.bp)
    app.register_blueprint(auth.bp)

    return app
