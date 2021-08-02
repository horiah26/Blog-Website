"""Can only access setup when no config file or as admin"""

from functools import wraps
from flask import redirect, url_for, flash
from config.config_db import ConfigDB
from config.config import Config
from services.auth import Authentication

config_db = ConfigDB()
config = Config()
auth = Authentication()

def setup_requirements(f):
    """decorator"""
    @wraps(f)
    def wrapped(*args, **kwargs):
        """decorator"""
        if config.config_file_exists():
            if Authentication().logged_user() != 'admin' and config_db.db_up_to_date():
                flash("Only admin can access this page")
                return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return wrapped
