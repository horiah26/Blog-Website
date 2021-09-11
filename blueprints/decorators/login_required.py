"""Only logged in user and admin have permission to modify user or user's posts"""
from functools import wraps
from flask import flash, redirect, url_for
from dependency_injector.wiring import inject, Provide


def login_required(f):
    """Only logged in user and admin have permission to modify user or user's posts"""

    @inject
    def get_auth(auth=Provide['auth']):
        return auth

    @wraps(f)
    def wrapped(*args, **kwargs):
        """Decorator"""
        try:
            if not get_auth().logged_user():
                flash("You must be logged in to do this", "error")
                return redirect(url_for('auth.login'))
        except:
            flash("You must be logged in to do this", "error")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)

    return wrapped
