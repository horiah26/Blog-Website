"""Edit_required only when email contains @temporary.com"""
from functools import wraps
from flask import session, flash, redirect, url_for

def edit_required_once(users_repo):
    """Edit_required only when email contains @temporary.com"""
    def decorator(f):
        """decorator"""
        @wraps(f)
        def wrapped(*args, **kwargs):
            """decorator"""
            if '@temporary.com' not in users_repo.get().get(session['username']).email:
                flash("User profile cannot be initialized")
                return redirect(url_for('blog.home'))
            return f(*args, **kwargs)
        return wrapped
    return decorator
