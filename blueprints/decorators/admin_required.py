"""Permission for admin only"""
from functools import wraps
from flask import redirect, url_for, flash
from dependency_injector.wiring import inject, Provide


def admin_required(f):
    """Permission for admin only"""

    @inject
    def get_auth(auth=Provide['auth']):
        return auth

    @wraps(f)
    def wrapped(*args, **kwargs):
        """Decorator"""
        if get_auth().logged_user() != 'admin':
            flash("Only admin has access to this page", "error")
            return redirect(url_for('blog.home'))
        return f(*args, **kwargs)

    return wrapped
