"""Edit_required only when email contains @temporary.com"""
from functools import wraps
from flask import session, flash, redirect, url_for
from dependency_injector.wiring import inject, Provide


def edit_required_once(f):
    """Edit_required only when email contains @temporary.com"""

    @wraps(f)
    @inject
    def wrapped(user_repo=Provide['user_repo'], *args, **kwargs):
        """Decorator"""
        if '@temporary.com' not in user_repo.get(session['username']).email:
            flash("User profile cannot be initialized", "error")
            return redirect(url_for('blog.home'))
        return f(*args, **kwargs)

    return wrapped
