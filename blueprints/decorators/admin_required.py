"""Only and admin has permission"""
from functools import wraps
from flask import redirect, url_for, flash, session
from dependency_injector.wiring import inject, Provide
 
def admin_required(f):
    """Only and admin has permission"""

    @inject
    def get_auth(auth = Provide['auth']):
        return auth

    @wraps(f)
    def wrapped(*args, **kwargs):
        """decorator"""
        if get_auth().logged_user() != 'admin':
            flash("Only admin has access to this page")
            return redirect(url_for('blog.home'))            
        return f(*args, **kwargs)
    return wrapped
