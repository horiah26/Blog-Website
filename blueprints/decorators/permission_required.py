"""Only logged in user and admin have permission to modify user or user's posts"""
from functools import wraps
from flask import redirect, url_for, flash, session
from containers.auth_container import AuthContainer

auth = AuthContainer().auth_factory()

def permission_required(repo_holder = None):
    """Only logged in user and admin have permission to modify user or user's posts"""
    def wrapping(f):
        """decorator"""
        @wraps(f)
        def wrapped(*args, **kwargs):
            """decorator"""
            if 'username' in kwargs:
                if 'username' not in session or auth.logged_user() != kwargs['username'] and auth.logged_user() != 'admin':
                    flash("You don't have permission to modify this profile")
                    return redirect(url_for('blog.home'))
            if 'post_id' in kwargs:
                if 'username' not in session or auth.logged_user() != repo_holder.get().get(kwargs['post_id'])[0].owner and auth.logged_user() != 'admin':
                    flash("You don't have permission to modify this post")
                    return redirect(url_for('blog.home'))
            return f(*args, **kwargs)
        return wrapped
    return wrapping
