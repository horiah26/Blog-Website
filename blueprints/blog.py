"""Blog blueprint"""
from flask import (
    Blueprint, flash, redirect, render_template, request, url_for, current_app, g
)
from flask_login import login_required, current_user
from repos.post.methods import post_misc_generator as gen
from models.post import Post
from models.repo_holder import RepoHolder
from database.connection import Connection
from blueprints.decorators.redirect_to_setup import redirect_to_setup
from blueprints.decorators.permission_required import permission_required

repo_holder = RepoHolder()
connection = Connection()
bp = Blueprint('blog', __name__)

@bp.route('/', methods=['GET'])
@redirect_to_setup
def home():
    """Route to home"""
    return render_template('blog/home.html', posts=repo_holder.get().get_previews(), generator=gen)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
@redirect_to_setup
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
            post_id = repo_holder.get().next_id()

            repo_holder.get().insert(Post(post_id, title, text, current_user.username))
            return redirect(url_for('blog.home'))
    return render_template('blog/create_post.html')

@bp.route('/<int:post_id>/', methods=['GET'])
@redirect_to_setup
def show(post_id):
    """Route to show post by id"""
    return render_template('blog/show_post.html', post=repo_holder.get().get(post_id))

@bp.route('/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
@redirect_to_setup
@permission_required(repo_holder)
def update(post_id):
    """Route to update existing posts"""
    post = repo_holder.get().get(post_id)
    if request.method == 'POST':
        title = request.form['title'].strip()
        text = request.form['text'].strip()

        if not title:
            title = post.title
        elif not text:
            text = post.text
        else:
            repo_holder.get().update(post_id, title, text)
            return redirect(url_for('blog.home'))
    return render_template('blog/update_post.html', post=post)

@bp.route('/<int:post_id>/delete', methods=['GET'])
@login_required
@redirect_to_setup
@permission_required(repo_holder)
def delete(post_id):
    """Route to delete posts"""
    repo_holder.get().delete(post_id)
    return redirect(url_for('blog.home'))
