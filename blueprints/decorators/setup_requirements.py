"""Can only access setup when no config file or as admin"""

from functools import wraps
from flask import redirect, url_for, flash
from containers.container import Container
from containers.auth_container import AuthContainer

container = Container()
config_db = container.config_db_factory()
config = container.config_factory()
auth = AuthContainer().auth_factory()

def setup_requirements(f):
    """decorator"""
    @wraps(f)
    def wrapped(*args, **kwargs):
        """decorator"""
        if config.config_file_exists():
            if auth.logged_user() != 'admin' and config_db.db_up_to_date():
                flash("Only admin can access this page")
                return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return wrapped
