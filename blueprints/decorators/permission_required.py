"""Only logged in user and admin have permission to modify user or user's posts"""
from functools import wraps
from flask_login import current_user
from flask import redirect, url_for, flash

def permission_required(repo_holder = None):
    """Only logged in user and admin have permission to modify user or user's posts"""
    def wrapping(f):
        """decorator"""
        @wraps(f)
        def wrapped(*args, **kwargs):
            """decorator"""
            if 'username' in kwargs:
                if current_user.username != kwargs['username'] and current_user.username != 'admin':
                    flash("You don't have permission to modify this profile")
                    return redirect(url_for('blog.home'))
            if 'post_id' in kwargs:
                if current_user.username != repo_holder.get().get(kwargs['post_id']).owner and current_user.username != 'admin':
                    flash("You don't have permission to modify this post")
                    return redirect(url_for('blog.home'))
            return f(*args, **kwargs)
        return wrapped
    return wrapping
