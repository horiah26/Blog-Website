"""Only and admin has permission"""
from functools import wraps
from flask import redirect, url_for, flash, session
from dependency_injector.wiring import inject, Provide
 
def admin_required(f):
    """Only and admin has permission"""
    @wraps(f)
    @inject
    def wrapped(auth = Provide['auth'], *args, **kwargs):
        """decorator"""
        if auth.logged_user() != 'admin':
            flash("Only admin has access to this page")
            return redirect(url_for('blog.home'))            
        return f(*args, **kwargs)
    return wrapped
