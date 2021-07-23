from flask_login import current_user
from functools import wraps
from flask import redirect, url_for


def permission_required(repo_holder = None):
    def wrapping(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if 'username' in kwargs:
                if current_user.username != kwargs['username'] and current_user.username != 'admin':
                    print("You don't have access to modify this profile")
                    return redirect(url_for('blog.home'))
            if 'post_id' in kwargs:
                if current_user.username != repo_holder.get().get(kwargs['post_id']).owner and current_user.username != 'admin':
                    print("You don't have access to modify this post")
                    return redirect(url_for('blog.home'))
            return f(*args, **kwargs)
        return wrapped
    return wrapping