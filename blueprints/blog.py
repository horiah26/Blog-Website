"""Blog blueprint"""
from flask import (
    Blueprint, flash, redirect, render_template, request, url_for, current_app
)

from repos.post.post_factory import PostFactory
from repos.post.methods import post_misc_generator as gen
from models.post import Post
from models.repo_holder import RepoHolder
from database.connection import db_config_missing

repo_holder = RepoHolder()

bp = Blueprint('blog', __name__)

@bp.route('/', methods=['GET'])
def home():
    """Route to home"""
    if repo_holder.posts is None and not db_config_missing():
        db_type = current_app.config["DB_TYPE"]
        repo_holder.posts = PostFactory.create_repo(db_type)

    if db_config_missing():
        return redirect(url_for('setup.setup_db'))
    return render_template('blog/home.html', posts=repo_holder.posts.get_previews(), generator=gen)

@bp.route('/create', methods=['GET', 'POST'])
def create():
    """Route to creating new posts"""
    if db_config_missing():
        return redirect(url_for('setup.setup_db'))
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
def show(post_id):
    """Route to show post by id"""
    if db_config_missing():
        return redirect(url_for('setup.setup_db'))
    return render_template('blog/show_post.html', post=repo_holder.posts.get(post_id))

@bp.route('/<int:post_id>/update', methods=['GET', 'POST'])
def update(post_id):
    """Route to update existing posts"""

    if db_config_missing():
        return redirect(url_for('setup.setup_db'))
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
def delete(post_id):
    """Route to delete posts"""
    if db_config_missing():
        return redirect(url_for('setup.setup_db'))
    repo_holder.posts.delete(post_id)
    return redirect(url_for('blog.home'))
