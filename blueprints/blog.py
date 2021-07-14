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
        title = request.form['title']
        text = request.form['text']
        error = None

        if not title:
            error = "Title is required"
        if not text:
            error = "Text is required"
        if error is not None:
            flash(error)
        else:
            id = posts.next_id()
            time_now = datetime.datetime.now().strftime("%H:%M  %d.%B.%Y")

            posts.insert(Post(id, title, text, "Owner", time_now, time_now))

            return redirect(url_for('blog.home'))

    return render_template('blog/create_post.html')

@bp.route('/<int:id>/', methods=['GET'])
def show(id):
    """Route to show post by id"""
    return render_template('blog/show_post.html', post=posts.get(id))

@bp.route('/<int:id>/update', methods=['GET', 'POST'])
def update(id):
    """Route to update existing posts"""
    post = posts.get(id)
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']

        if not title:
            title = post.title
        elif not text:
            text = post.text
        else:
            date_modified = datetime.datetime.now().strftime("Last edited at: %H:%M %d.%B.%Y")
            posts.update(id, title, text, date_modified)

            return redirect(url_for('blog.home'))
    return render_template('blog/update_post.html', post=post)

@bp.route('/<int:id>/delete', methods=['GET'])
def delete(id):
    """Route to delete posts"""
    posts.delete(id)
    return redirect(url_for('blog.home'))
