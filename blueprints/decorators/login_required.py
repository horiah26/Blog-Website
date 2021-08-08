"""Only logged in user and admin have permission to modify user or user's posts"""
from functools import wraps
from flask import flash, redirect, url_for
from containers.auth_container import AuthContainer

auth_service = AuthContainer().auth_factory()

def login_required(f):
    """decorator"""
    @wraps(f)
    def wrapped(*args, **kwargs):
        """decorator"""
        try:
            if not auth_service.logged_user():
                flash("You must be logged in to do this")
                return redirect(url_for('auth.login'))
        except Exception:
            flash("You must be logged in to do this")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return wrapped
