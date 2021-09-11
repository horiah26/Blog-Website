"""Redirects to setup page if db not configured"""
from functools import wraps
from flask import redirect, url_for
from dependency_injector.wiring import inject, Provide

def redirect_to_setup(f):
    """Redirects to setup page if db not configured"""

    @inject
    def get_config(config = Provide['config']):
        return config

    @inject
    def get_config_db(config_db = Provide['config_db']):
        return config_db

    @wraps(f)
    def redirect_if_no_db(*args, **kwargs):
        """Decorator"""
        if not get_config().config_file_exists():
            return redirect(url_for('setup.setup_db'))

        return f(*args, **kwargs)
    return redirect_if_no_db
