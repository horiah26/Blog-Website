"""Only logged in user and admin have permission to modify user or user's posts"""
from functools import wraps
from flask import flash, redirect, url_for
from dependency_injector.wiring import inject, Provide

def login_required(f):
    """decorator"""
    
    @inject
    def get_auth(auth = Provide['auth']):
        return auth

    @wraps(f)
    def wrapped(*args, **kwargs):
        """decorator"""
        try:
            if not get_auth().logged_user():
                flash("You must be logged in to do this")
                return redirect(url_for('auth.login'))
        except Exception:
            flash("You must be logged in to do this")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return wrapped
