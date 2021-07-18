"""Blog blueprint"""
from functools import wraps
from flask import (
    Blueprint, flash, redirect, render_template, request, url_for, current_app
)
from repos.post.methods import post_misc_generator as gen
from models.post import Post
from models.repo_holder import RepoHolder
from database.connection import Connection

repo_holder = RepoHolder()
connection = Connection()

bp = Blueprint('blog', __name__)

def check_repo(f):
    """Creates posts repository if it doesn't exist"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        """Creates posts repository if it doesn't exist"""
        if repo_holder.posts is None:
            repo_holder.create_repo(current_app)
        return f(*args, **kwargs)
    return decorated_function

def redirect_to_setup(f):
    """Redirects to setup page if db not configured"""
    @wraps(f)
    def redirect_if_no_db(*args, **kwargs):
        """Redirects to setup page if db not configured"""
        if not connection.db_config_exists(current_app):
            return redirect(url_for('setup.setup_db'))
        return f(*args, **kwargs)
    return redirect_if_no_db

@bp.route('/', methods=['GET'])
@redirect_to_setup
@check_repo
def home():
    """Route to home"""
    return render_template('blog/home.html', posts=repo_holder.posts.get_previews(), generator=gen)

@bp.route('/create', methods=['GET', 'POST'])
@redirect_to_setup
@check_repo
def create():
    """Route to creating new posts"""
    if request.method == 'POST':
        title = request.form['title'].strip()
        text = request.form['text'].strip()

        error = None
        if not title:
            error = "Title is required"
        if not text:
            error = "Text is required"
        if error is not None:
            flash(error)
        else:
            post_id = repo_holder.posts.next_id()

            repo_holder.posts.insert(Post(post_id, title, text, "Owner"))
            return redirect(url_for('blog.home'))
    return render_template('blog/create_post.html')

@bp.route('/<int:post_id>/', methods=['GET'])
@redirect_to_setup
@check_repo
def show(post_id):
    """Route to show post by id"""
    return render_template('blog/show_post.html', post=repo_holder.posts.get(post_id))

@bp.route('/<int:post_id>/update', methods=['GET', 'POST'])
@redirect_to_setup
@check_repo
def update(post_id):
    """Route to update existing posts"""
    post = repo_holder.posts.get(post_id)
    if request.method == 'POST':
        title = request.form['title'].strip()
        text = request.form['text'].strip()

        if not title:
            title = post.title
        elif not text:
            text = post.text
        else:
            repo_holder.posts.update(post_id, title, text)
            return redirect(url_for('blog.home'))
    return render_template('blog/update_post.html', post=post)

@bp.route('/<int:post_id>/delete', methods=['GET'])
@redirect_to_setup
@check_repo
def delete(post_id):
    """Route to delete posts"""
    repo_holder.posts.delete(post_id)
    return redirect(url_for('blog.home'))
