"""Edit_required only when email contains @temporary.com"""
from functools import wraps
from flask import session, flash, redirect, url_for
from dependency_injector.wiring import inject, Provide

def edit_required_once(f):
    """Edit_required only when email contains @temporary.com"""

    def get_repo(users_repo = Provide['user_repo_holder']):
        return users_repo
        
    @wraps(f)
    def wrapped(*args, **kwargs):
        """decorator"""
        if '@temporary.com' not in get_repo().get().get(session['username']).email:
            flash("User profile cannot be initialized")
            return redirect(url_for('blog.home'))
        return f(*args, **kwargs)
    return wrapped
