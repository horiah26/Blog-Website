"""Creates instance of Flask app"""
from flask import Flask
from blueprints import setup
from blueprints import users
from blueprints import blog
from blueprints import auth
from containers.container import Container

from repos.post import post_repo_db
from repos.post import post_repo_alchemy
from repos.post import post_repo_memory
from models import post_repo_holder
from repos.user import user_repo_db
from repos.user import user_repo_alchemy
from repos.user import user_repo_memory
from models import user_repo_holder
from database import database
from database import hash_imported_passwords
from services import auth
from config import config
from blueprints import setup
from blueprints import users
from blueprints import blog
from blueprints import auth as bp_auth
from blueprints.decorators import setup_requirements
from blueprints.decorators import permission_required
from blueprints.decorators import admin_required
from blueprints.decorators import login_required
from blueprints.decorators import edit_required_once

def create_app():
    """Creates app"""
    database_type = "db"

    container = Container()
    container.wire(modules = [post_repo_db, user_repo_db, database, setup, blog, auth, bp_auth, admin_required, setup_requirements, permission_required, login_required, users, post_repo_alchemy, user_repo_alchemy, hash_imported_passwords, post_repo_holder, user_repo_holder, edit_required_once, post_repo_memory, user_repo_memory, config])
    app=Flask(__name__, template_folder='templates')
    app.config.from_mapping(
        SECRET_KEY="secret",
        DB_TYPE = database_type)
    app.container = container
    app.app_context().push()

    if database_type == "db" or database_type == "alchemy":
        @app.before_first_request
        def create_tables():
            database.Database().create_update_tables()

    app.register_blueprint(setup.bp)
    app.register_blueprint(users.bp)
    app.register_blueprint(blog.bp)
    app.register_blueprint(bp_auth.bp)

    return app
