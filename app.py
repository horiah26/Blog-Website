"""Creates instance of Flask app"""
from flask import Flask
from blueprints import setup
from blueprints import users
from blueprints import blog
from blueprints import auth
from containers.db_container import DBContainer

def create_app():
    """Creates app"""
    database_type = "db"

    app=Flask(__name__, template_folder='templates')
    app.config.from_mapping(
        SECRET_KEY="secret",
        DB_TYPE = database_type)
    app.app_context().push()

    if database_type == "db" or database_type == "alchemy":
        @app.before_first_request
        def create_tables():
            DBContainer().database_factory().create_update_tables()

    app.register_blueprint(setup.bp)
    app.register_blueprint(users.bp)
    app.register_blueprint(blog.bp)
    app.register_blueprint(auth.bp)

    return app
