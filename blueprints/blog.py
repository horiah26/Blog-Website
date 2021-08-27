"""Blog blueprint"""
from flask import (
    Blueprint, flash, redirect, render_template, request, url_for, session
)
from dependency_injector.wiring import inject, Provide

from repos.post.methods import post_misc_generator as gen
from blueprints.decorators.redirect_to_setup import redirect_to_setup
from blueprints.decorators.permission_required import permission_required
from blueprints.decorators.login_required import login_required

from models.post import Post

bp = Blueprint('blog', __name__)

@bp.route('/', methods=['GET', 'POST'])
@redirect_to_setup
@inject
def home(post_repo = Provide['post_repo'], user_repo = Provide['user_repo']):
    """Route to home + pagination + filter by user"""
    if 'filter_user' not in session:
        session['filter_user'] = None

    page_num = request.args.get('page', 1, type=int)

    if request.method == 'POST':
        if request.form['action'] == 'Search':
            session['filter_user'] = request.form['user'].strip()
            page_num = 1
        if request.form['action'] == 'Reset':
            session['filter_user'] = None
            page_num = 1

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
def create(auth = Provide['auth'], post_repo = Provide['post_repo'], img_repo = Provide['img_repo']):
    """Route to creating new posts"""
    if request.method == 'POST':
        title = request.form['title'].strip()
        text = request.form['text'].strip()
        img_id = 0

        if 'img' in request.files:
            image = request.files['img']
            if image.filename != '':
                if img_repo.allowed_file(image.filename):
                    img_id = img_repo.save(image)
                else:
                    flash("File format not supported. Format must be one of the following: png, jpg, jpeg, gif, bmp", "error")
                    return redirect(url_for('blog.create'))

        error = None
        if not title:
            error = "Title is required"
        if not text:
            error = "Text is required"
        if error is not None:
            flash(error, "error")
        else:
            post_id = post_repo.next_id()

            post_repo.insert(Post(post_id, title, text, auth.logged_user(), img_id))

            flash("Post has been created")
            return redirect(url_for('blog.home'))
    return render_template('blog/create_post.html')

@bp.route('/<int:post_id>/', methods=['GET'])
@redirect_to_setup
@inject
def show(post_id, post_repo = Provide['post_repo']):
    """Route to show post by id"""
    if post_repo.get(post_id) is None:
        flash("Post not found")
        return redirect(url_for('blog.home'))
    return render_template('api/api_post.html', post_id = post_id)

@bp.route('/<int:post_id>/update', methods=['GET', 'POST'])
@redirect_to_setup
@permission_required
@inject
def update(post_id, post_repo = Provide['post_repo'], img_repo = Provide['img_repo']):
    """Route to update existing posts"""
    post = post_repo.get(post_id)[0]
    img_id = post.img_id
    if request.method == 'POST':
        title = request.form['title'].strip()
        text = request.form['text'].strip()

        if 'img' in request.files:
            image = request.files['img']
            if image.filename != '':
                if img_repo.allowed_file(image.filename):
                    img_id = img_repo.save(image)
                else:
                    flash("File format not supported. Format must be one of the following: png, jpg, jpeg, gif, bmp", "error")
                    return redirect(url_for('blog.update', post_id = post_id))

        if not title:
            title = post.title
        if not text:
            text = post.text
        else:
            post_repo.update(post_id, title, text, img_id)
            img_repo.delete_unused()
            flash("Post has been updated")
            return redirect(url_for('blog.home'))
    return render_template('blog/update_post.html', post=post)

@bp.route('/<int:post_id>/delete', methods=['GET'])
@redirect_to_setup
@permission_required
@inject
def delete(post_id, post_repo = Provide['post_repo'], img_repo = Provide['img_repo']):
    """Route to delete posts"""
    post_repo.delete(post_id)
    img_repo.delete_unused()
    flash("Post has been deleted")
    return redirect(url_for('blog.home'))

@bp.route('/statistics', methods=['GET'])
@login_required
@redirect_to_setup
@inject
def statistics(statistics = Provide['statistics']):
    """Route to delete posts"""
    return render_template('blog/statistics.html', statistics=statistics.get())
