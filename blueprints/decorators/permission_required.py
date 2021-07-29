"""Only logged in user and admin have permission to modify user or user's posts"""
from functools import wraps
from flask import redirect, url_for, flash, session

def permission_required(repo_holder = None):
    """Only logged in user and admin have permission to modify user or user's posts"""
    def wrapping(f):
        """decorator"""
        @wraps(f)
        def wrapped(*args, **kwargs):
            """decorator"""
            if 'username' in kwargs:
                if 'username' not in session or session['username'] != kwargs['username'] and session['username'] != 'admin':
                    flash("You don't have permission to modify this profile")
                    return redirect(url_for('blog.home'))
            if 'post_id' in kwargs:
                if 'username' not in session or session['username'] != repo_holder.get().get(kwargs['post_id'])[0].owner and session['username'] != 'admin':
                    flash("You don't have permission to modify this post")
                    return redirect(url_for('blog.home'))
            return f(*args, **kwargs)
        return wrapped
    return wrapping
