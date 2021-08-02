"""Redirects to setup page if db not configured"""
from functools import wraps
from flask import redirect, url_for
from database.database import Database
from config.config import Config
from config.config_db import ConfigDB

config = Config()
database = Database()
def redirect_to_setup(f):
    """Added so app could be inserted as a parameter in the other wrapper"""
    @wraps(f)
    def redirect_if_no_db(*args, **kwargs):
        """Redirects to setup page if db not configured"""
        if not config.config_file_exists() or not ConfigDB().db_up_to_date():
            return redirect(url_for('setup.setup_db'))

        return f(*args, **kwargs)
    return redirect_if_no_db
