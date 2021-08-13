"""Creates instance of Flask app"""
from flask import Flask
from blueprints import setup
from blueprints import users
from blueprints import blog
from blueprints import auth

from services.init_injection import InitInjection
from database.database import Database

def create_app():
    """Creates app"""
    database_type = "db"

    app=Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY="secret",
        DB_TYPE = database_type)
    app.container = InitInjection(database_type).get_container()
    app.app_context().push()
    
    @app.before_first_request
    def create_tables():
        if database_type in ["db", "alchemy"]:
            Database().create_update_tables()

    app.register_blueprint(setup.bp)
    app.register_blueprint(users.bp)
    app.register_blueprint(blog.bp)
    app.register_blueprint(auth.bp)

    return app
