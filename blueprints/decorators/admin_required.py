"""Only and admin has permission"""
from functools import wraps
from flask import redirect, url_for, flash, session
from containers.auth_container import AuthContainer

auth = AuthContainer().auth_factory()

def admin_required(f):
    """Only and admin has permission"""
    @wraps(f)
    def wrapped(*args, **kwargs):
        """decorator"""
        if auth.logged_user() != 'admin':
            flash("Only admin has access to this page")
            return redirect(url_for('blog.home'))            
        return f(*args, **kwargs)
    return wrapped
