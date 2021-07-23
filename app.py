"""Creates instance of Flask app"""
from flask import Flask
from models.user import User
from flask_login import LoginManager
from blueprints import setup
from blueprints import users
from blueprints import blog
from repos.user.user_repo_factory import UserRepoFactory

def create_app():
    """Creates app"""
    app=Flask(__name__, template_folder='templates')
    app.config.from_mapping(
        SECRET_KEY="secret",
        DB_TYPE = "db")
    app.app_context().push()

    login_manager = LoginManager(app)
    user_repo = UserRepoFactory.create_repo(app.config['DB_TYPE'])
    @login_manager.user_loader
    def load_user(username):
        return user_repo.get(username)
    login_manager.login_view = 'users.login'

    app.register_blueprint(setup.bp)
    app.register_blueprint(users.bp)
    app.register_blueprint(blog.bp)
    return app
