"""Only logged in user and admin have permission to modify user or user's posts"""
from functools import wraps
from flask import session, flash, redirect, url_for
from services.auth import Authentication

def login_required(f):
    """decorator"""
    @wraps(f)
    def wrapped(*args, **kwargs):
        """decorator"""
        try:
            Authentication().logged_user()
        except Exception:
            flash("You must be logged in to do this")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return wrapped
