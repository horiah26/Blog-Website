"""Blueprint for user management"""
from flask import (
    Blueprint, redirect, render_template, request, url_for, flash,
)
from werkzeug.security import generate_password_hash
from blueprints.decorators.redirect_to_setup import redirect_to_setup
from blueprints.decorators.permission_required import permission_required
from blueprints.decorators.edit_required_once import edit_required_once
from blueprints.decorators.admin_required import admin_required
from repos.post.methods import post_misc_generator as gen
from containers.repo_holder_container import RepoHolderContainer
from containers.auth_container import AuthContainer

auth = AuthContainer().auth_factory()
repo_holder_container = RepoHolderContainer()
users_repo = repo_holder_container.user_repo_holder_factory()
posts_repo = repo_holder_container.post_repo_holder_factory()

bp = Blueprint('users', __name__)

@bp.route('/users', methods=['GET'])
@admin_required
@redirect_to_setup
def view_all():
    """View all users"""
    return render_template('users/view_all.html', users = users_repo.get().get_all())

@bp.route('/users/<username>/', methods=['GET'])
@redirect_to_setup
def view_user(username):
    """View user"""
    per_page = 6
    page_num = request.args.get('page', 1, type=int)
    previews_pages = posts_repo.get().get_previews(username, per_page, page_num)
    previews = previews_pages[0]
    total_pages = previews_pages[1]
    
    print(total_pages, "pages")
    if total_pages == 1:
        pages = [1]
        print(pages)
    else:
        pages = range (1, total_pages + 1)

    if page_num not in pages:
        page_num = 1

    if users_repo.get().get(username):
        return render_template('users/view.html', user = users_repo.get().get(username),page_num = page_num, pages = pages, posts = previews, generator = gen)
    flash('User not found')
    return redirect(url_for('users.view_all'))

@bp.route('/users/<username>/delete', methods=['GET'])
@redirect_to_setup
@permission_required()
def delete(username):
    """Delete user"""
    if username == 'admin':
        flash("Admin cannot be deleted")
    else:
        try:
            users_repo.get().delete(username)
            flash("User deleted")
            auth.logout()
        except Exception:
            flash("Delete user's posts first")
    return redirect(url_for('blog.home'))

@bp.route('/users/<username>/edit', methods=['GET', 'POST'])
@redirect_to_setup
@permission_required()
def edit(username):
    """Edit user"""
    user = users_repo.get().get(username)
    if user.username != auth.logged_user() and auth.logged_user() != 'admin':
        print('Only the User cand edit their post')
        return redirect(url_for('blog.home'))

    if request.method == 'POST':
        email = request.form['email'].strip()
        name = request.form['name'].strip()
        password = request.form['password'].strip()
        confirm_password = request.form['confirm_password'].strip()

        error = None
        if password != confirm_password:
            error = "Password must match"
        if error is not None:
            print(error)
            flash(error)
        else:
            if not name:
                name = user.name
            elif not email:
                email = user.email
            if not password:
                users_repo.get().update(username, name, email, user.password)
            else:
                users_repo.get().update(username, name, email, generate_password_hash(password, method='pbkdf2:sha512:100'))
            flash("User profile has been modified")
            return redirect(url_for('users.view_user', username = user.username))
    return render_template('auth/edit.html', user = user)

@bp.route('/users/<username>/edit_required', methods=['GET', 'POST'])
@redirect_to_setup
@permission_required()
@edit_required_once(users_repo)
def edit_required(username):
    """Edit user"""
    user = users_repo.get().get(username)
    if user.username != auth.logged_user() and auth.logged_user() != 'admin':
        print('Only the User cand edit their post')
        return redirect(url_for('blog.home'))

    if request.method == 'POST':
        email = request.form['email'].strip()
        name = request.form['name'].strip()
        password = request.form['password'].strip()
        confirm_password = request.form['confirm_password'].strip()

        error = None
        if password != confirm_password:
            error = "Password does not match"
        if not password:
            error = "Password is required"
        if not email:
            error = "Email is required"
        if not name:
            error = "Name is required"
        if error is not None:
            flash(error)
        else:
            users_repo.get().update(username, name, email, generate_password_hash(password, method='pbkdf2:sha512:100'))
            flash("User profile has been modified")
            return redirect(url_for('users.view_user', username = user.username))
    return render_template('auth/edit_required.html', user = user)
