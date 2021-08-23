"""Creates instance of Flask app"""
from flask import Flask
from blueprints import setup
from blueprints import users
from blueprints import blog
from blueprints import auth

from services.init_injection import InitInjection

def create_app():
    """Creates app"""
    database_type = "db"

    container = InitInjection(database_type).get_container()

    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY = "secret key",
        UPLOAD_FOLDER = 'static/uploads',
        DB_TYPE = database_type)
    app.container = container    
    app.app_context().push()
    
    if database_type in ["db", "alchemy"]:
        db = container.database()
        db.create_update_tables()

    app.register_blueprint(setup.bp)
    app.register_blueprint(users.bp)
    app.register_blueprint(blog.bp)
    app.register_blueprint(auth.bp)

    return app
