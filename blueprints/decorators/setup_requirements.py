"""Can only access setup when no config file or as admin"""

from functools import wraps
from flask import redirect, url_for, flash
from dependency_injector.wiring import inject, Provide

def setup_requirements(f):
    """decorator"""

    @inject
    def get_auth(auth = Provide['auth']):
        return auth

    @inject
    def get_config_db(config_db = Provide['config_db']):
        return config_db

    @inject
    def get_config(config = Provide['config']):
        return config

    @wraps(f)
    @inject
    def wrapped(*args, **kwargs):
        """decorator"""
        if get_config().config_file_exists():
            if get_auth().logged_user() != 'admin' and get_config_db().db_up_to_date():
                flash("Only admin can access this page")
                return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return wrapped
