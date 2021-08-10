"""Blog blueprint"""
import math
from flask import (
    Blueprint, flash, redirect, render_template, request, url_for, session
)
from repos.post.methods import post_misc_generator as gen
from blueprints.decorators.redirect_to_setup import redirect_to_setup
from blueprints.decorators.permission_required import permission_required
from blueprints.decorators.login_required import login_required
from containers.container import Container
from containers.db_container import DBContainer
from containers.auth_container import AuthContainer
from containers.repo_holder_container import RepoHolderContainer

container = Container()
auth = AuthContainer().auth_factory()
post_repo_holder = RepoHolderContainer().post_repo_holder_factory()
user_repo_holder = RepoHolderContainer().user_repo_holder_factory()
db = DBContainer().database_factory()

bp = Blueprint('blog', __name__)

@bp.route('/', methods=['GET', 'POST'])
@redirect_to_setup
def home():
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
    previews_pages = post_repo_holder.get().get_previews(session['filter_user'], per_page, page_num)

    previews = previews_pages[0]

    total_pages = previews_pages[1]
    pages = range (1, total_pages + 1)
    if page_num not in pages:
        page_num = 1

    users = user_repo_holder.get().get_all()
    return render_template('blog/home.html', posts = previews, users = users, page_num = page_num, pages = pages, generator=gen)

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
            post_id = post_repo_holder.get().next_id()

            post_repo_holder.get().insert(container.post_factory(post_id, title, text, auth.logged_user()))

            flash("Post has been created")
            return redirect(url_for('blog.home'))
    return render_template('blog/create_post.html')

@bp.route('/<int:post_id>/', methods=['GET'])
@redirect_to_setup
def show(post_id):
    """Route to show post by id"""
    post_and_display_name = post_repo_holder.get().get(post_id)
    if post_and_display_name:
        return render_template('blog/show_post.html', post = post_and_display_name[0], display_name = post_and_display_name[1])
    flash('Post not found')
    return redirect(url_for('blog.home'))

@bp.route('/<int:post_id>/update', methods=['GET', 'POST'])
@redirect_to_setup
@permission_required(post_repo_holder)
def update(post_id):
    """Route to update existing posts"""
    post = post_repo_holder.get().get(post_id)
    if request.method == 'POST':
        title = request.form['title'].strip()
        text = request.form['text'].strip()

        if not title:
            title = post.title
        elif not text:
            text = post.text
        else:
            post_repo_holder.get().update(post_id, title, text)
            flash("Post has been updated")
            return redirect(url_for('blog.home'))
    return render_template('blog/update_post.html', post=post[0])

@bp.route('/<int:post_id>/delete', methods=['GET'])
@redirect_to_setup
@permission_required(post_repo_holder)
def delete(post_id):
    """Route to delete posts"""
    post_repo_holder.get().delete(post_id)
    flash("Post has been deleted")
    return redirect(url_for('blog.home'))

@bp.route('/filter', methods=['GET', 'POST'])
@redirect_to_setup
@permission_required(post_repo_holder)
def filter():
    """Search function"""
    username = ''
    if request.method == 'POST':
        print(request.form, " Req form")
        if request.form['action'] == 'Search':
            username = request.form['user'].strip()

    user = user_repo_holder.get().get(username)
    users = user_repo_holder.get().get_all()
    users.insert(0, None)
    if user is None and username != '':
        flash('Please enter a valid username')
    return render_template('blog/filter_view.html', user = user, posts = post_repo_holder.get().get_previews(username), users = user_repo_holder.get().get_all(), generator = gen)
