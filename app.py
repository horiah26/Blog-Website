"""Creates instance of Flask app"""
from flask import Flask
from blueprints import setup
from blueprints import users
from blueprints import blog
from blueprints import auth

from services.init_injection import InitInjection

def create_app():
    """Creates app"""
    database_type = "memory"

    container = InitInjection(database_type).get_container()

    UPLOAD_FOLDER = 'static/uploads'

    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY="secret",
        UPLOAD_FOLDER = UPLOAD_FOLDER,
        DB_TYPE = database_type)
    app.container = container    
    app.app_context().push()
    
    if database_type in ["db", "alchemy"]:
        container.database.create_update_tables()

    app.register_blueprint(setup.bp)
    app.register_blueprint(users.bp)
    app.register_blueprint(blog.bp)
    app.register_blueprint(auth.bp)

    return app
