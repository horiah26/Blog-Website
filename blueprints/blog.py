"""Blog blueprint"""
import math
from flask import (
    Blueprint, flash, redirect, render_template, request, url_for, session
)
from repos.post.methods import post_misc_generator as gen
from blueprints.decorators.redirect_to_setup import redirect_to_setup
from blueprints.decorators.permission_required import permission_required
from blueprints.decorators.login_required import login_required
from dependency_injector.wiring import inject, Provide

from models.post import Post
from models.post_preview import PostPreview
from models.user import User

bp = Blueprint('blog', __name__)

@bp.route('/', methods=['GET', 'POST'])
@redirect_to_setup
@inject
def home(post_repo = Provide['post_repo'], user_repo = Provide['user_repo']):
    """Route to home + pagination + filter by user"""
    if not 'filter_user' in session:        
            session['filter_user'] = None

    page_num = request.args.get('page', 1, type=int)

    if request.method == 'POST':
        if request.form['action'] == 'Search':
            session['filter_user'] = request.form['user'].strip()
            page_num = 1;
        if request.form['action'] == 'Reset':
            session['filter_user'] = None
            page_num = 1;
        
    per_page = 6
    previews_pages = post_repo.get_previews(session['filter_user'], per_page, page_num)

    previews = previews_pages[0]

    total_pages = previews_pages[1]
    pages = range (1, total_pages + 1)
    if page_num not in pages:
        page_num = 1
    return render_template('blog/home.html', posts = previews, users = user_repo.get_users_with_posts(), page_num = page_num, pages = pages, generator=gen)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
@redirect_to_setup
@inject
def create(auth = Provide['auth'], post_repo = Provide['post_repo']):
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
            post_id = post_repo.next_id()

            post_repo.insert(Post(post_id, title, text, auth.logged_user()))

            flash("Post has been created")
            return redirect(url_for('blog.home'))
    return render_template('blog/create_post.html')

@bp.route('/<int:post_id>/', methods=['GET'])
@redirect_to_setup
@inject
def show(post_id, post_repo = Provide['post_repo']):
    """Route to show post by id"""
    post_and_display_name = post_repo.get(post_id)
    if post_and_display_name:
        return render_template('blog/show_post.html', post = post_and_display_name[0], display_name = post_and_display_name[1])
    flash('Post not found')
    return redirect(url_for('blog.home'))

@bp.route('/<int:post_id>/update', methods=['GET', 'POST'])
@redirect_to_setup
@permission_required
@inject
def update(post_id, post_repo = Provide['post_repo']):
    """Route to update existing posts"""
    post = post_repo.get(post_id)[0]
    if request.method == 'POST':
        title = request.form['title'].strip()
        text = request.form['text'].strip()

        if not title:
            title = post.title
        elif not text:
            print(post)
            text = post.text
        else:
            post_repo.update(post_id, title, text)
            flash("Post has been updated")
            return redirect(url_for('blog.home'))
    return render_template('blog/update_post.html', post=post)

@bp.route('/<int:post_id>/delete', methods=['GET'])
@redirect_to_setup
@permission_required
@inject
def delete(post_id, post_repo = Provide['post_repo']):
    """Route to delete posts"""
    post_repo.delete(post_id)
    flash("Post has been deleted")
    return redirect(url_for('blog.home'))
