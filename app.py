"""Creates instance of Flask app"""
from flask import Flask

def create_app():
    """Creates app"""
    app=Flask(__name__, template_folder='templates')
    app.config.from_mapping(
        SECRET_KEY="secret")
    from blueprints import blog
    app.register_blueprint(blog.bp)
    return app
