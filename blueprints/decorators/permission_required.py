"""Only logged in user and admin have permission to modify user or user's posts"""
from functools import wraps
from flask import redirect, url_for, flash, session
from dependency_injector.wiring import inject, Provide

    
def permission_required(f):
    """decorator"""
    
    @inject
    def get_auth(auth = Provide['auth']):
        return auth

    @inject
    def get_post_repo(post_repo = Provide['post_repo']):
        return post_repo

    @wraps(f)
    def wrapped(*args, **kwargs):
        
        """decorator"""
        auth = get_auth()
        if 'username' in kwargs:
            if 'username' not in session or auth.logged_user() != kwargs['username'] and auth.logged_user() != 'admin':
                flash("You don't have permission to modify this profile")
                return redirect(url_for('blog.home'))
        if 'post_id' in kwargs:
            if 'username' not in session or auth.logged_user() != get_post_repo().get(kwargs['post_id'])[0].owner and auth.logged_user() != 'admin':
                flash("You don't have permission to modify this post")
                return redirect(url_for('blog.home'))
        return f(*args, **kwargs)
    return wrapped