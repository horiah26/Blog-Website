"""Blog blueprint"""
import datetime
from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)

from repos.post.post_factory import PostFactory
from repos.post.methods.preview import preview
from repos.post.methods import post_misc_generator as gen
from models.post import Post

posts = PostFactory.create_repo("memory")

bp = Blueprint('blog', __name__)
@bp.route('/', methods=['GET'])
def home():
    """Route to home"""
    return render_template('blog/home.html', posts=posts.get_all(), preview=preview, generator=gen)

@bp.route('/create', methods=['GET', 'POST'])
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
            post_id = posts.next_id()

            posts.insert(Post(post_id, title, text, "Owner"))

            return redirect(url_for('blog.home'))

    return render_template('blog/create_post.html')

@bp.route('/<int:post_id>/', methods=['GET'])
def show(post_id):
    """Route to show post by id"""
    return render_template('blog/show_post.html', post=posts.get(post_id))

@bp.route('/<int:post_id>/update', methods=['GET', 'POST'])
def update(post_id):
    """Route to update existing posts"""
    post = posts.get(post_id)
    if request.method == 'POST':
        title = request.form['title'].strip()
        text = request.form['text'].strip()

        if not title:
            title = post.title
        elif not text:
            text = post.text
        else:
            date_modified = datetime.datetime.now().strftime("%H:%M %B %d %Y")
            posts.update(post_id, title, text, date_modified)

            return redirect(url_for('blog.home'))
    return render_template('blog/update_post.html', post=post)

@bp.route('/<int:post_id>/delete', methods=['GET'])
def delete(post_id):
    """Route to delete posts"""
    posts.delete(post_id)
    return redirect(url_for('blog.home'))
