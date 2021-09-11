"""Blueprint for user management"""
from flask import (
    Blueprint, redirect, render_template, request, url_for, flash,
)
from dependency_injector.wiring import inject, Provide

from blueprints.decorators.redirect_to_setup import redirect_to_setup
from blueprints.decorators.permission_required import permission_required
from blueprints.decorators.edit_required_once import edit_required_once
from blueprints.decorators.admin_required import admin_required
from repos.post.methods import post_misc_generator as gen

bp = Blueprint('users', __name__)


@bp.route('/users', methods=['GET'])
@admin_required
@redirect_to_setup
@inject
def view_all(auth=Provide['auth'], user_repo=Provide['user_repo']):
    """View all users"""
    users = user_repo.get_all()
    print(users[0].img_id)
    return render_template('users/view_all.html', users=user_repo.get_all(), auth=auth)


@bp.route('/users/<username>/', methods=['GET'])
@redirect_to_setup
@inject
def view_user(username, user_repo=Provide['user_repo'], post_repo=Provide['post_repo']):
    """View user"""
    per_page = 6
    page_num = request.args.get('page', 1, type=int)
    previews_pages = post_repo.get_previews(username, per_page, page_num)
    previews = previews_pages[0]
    total_pages = previews_pages[1]

    if total_pages == 1:
        pages = [1]
    else:
        pages = range(1, total_pages + 1)

    if page_num not in pages:
        page_num = 1

    if user_repo.get(username):
        return render_template('users/view.html', user=user_repo.get(username), page_num=page_num, pages=pages,
                               posts=previews, generator=gen)
    flash('User not found', "error")
    return redirect(url_for('users.view_all'))


@bp.route('/users/<username>/delete', methods=['GET'])
@redirect_to_setup
@permission_required
@inject
def delete(username, auth=Provide['auth'], user_repo=Provide['user_repo']):
    """Delete user"""
    if username == 'admin':
        flash("Admin cannot be deleted", "error")
    else:
        try:
            user_repo.delete(username)
            flash("User deleted")
            if username != 'admin':
                auth.logout()
        except:
            flash("Delete user's posts first", "error")
    return redirect(url_for('blog.home'))


@bp.route('/users/<username>/edit', methods=['GET', 'POST'])
@redirect_to_setup
@permission_required
@inject
def edit(username, auth=Provide['auth'], user_repo=Provide['user_repo'], hasher=Provide['hasher'],
         user_img=Provide['profile_img_repo']):
    """Edit user"""
    user = user_repo.get(username)
    img_id = user.img_id
    if user.username != auth.logged_user() and auth.logged_user() != 'admin':
        flash('Only the User cand edit their post', "error")
        return redirect(url_for('blog.home'))

    if request.method == 'POST':
        email = request.form['email'].strip()
        name = request.form['name'].strip()
        password = request.form['password'].strip()
        confirm_password = request.form['confirm_password'].strip()

        if 'img' in request.files:
            image = request.files['img']
            if image.filename != '':
                if user_img.allowed_file(image.filename):
                    img_id = user_img.save(image)
                else:
                    flash("File format not supported. Format must be one of the following: png, jpg, jpeg, gif, bmp",
                          "error")
                    return redirect(url_for('auth.sign_up'))

        if password != confirm_password:
            flash("Password must match", "error")
        else:
            if not name:
                name = user.name
            if not email:
                email = user.email
            if not password:
                user_repo.update(username, name, email, img_id, user.password)
            else:
                user_repo.update(username, name, email, img_id, hasher.hash(password))
            flash("User profile has been modified")
            return redirect(url_for('users.view_user', username=user.username))
    return render_template('auth/edit.html', user=user)


@bp.route('/users/<username>/edit_required', methods=['GET', 'POST'])
@redirect_to_setup
@permission_required
@edit_required_once
@inject
def edit_required(username, auth=Provide['auth'], user_repo=Provide['user_repo'], hasher=Provide['hasher'],
                  user_img=Provide['profile_img_repo']):
    """Edit is required"""
    user = user_repo.get(username)
    img_id = user.img_id
    if user.username != auth.logged_user() and auth.logged_user() != 'admin':
        print('Only the User can edit their post')
        return redirect(url_for('blog.home'))

    if request.method == 'POST':
        email = request.form['email'].strip()
        name = request.form['name'].strip()
        password = request.form['password'].strip()
        confirm_password = request.form['confirm_password'].strip()

        if 'img' in request.files:
            image = request.files['img']
            if image.filename != '':
                if user_img.allowed_file(image.filename):
                    img_id = user_img.save(image)
                else:
                    flash("File format not supported. Format must be one of the following: png, jpg, jpeg, gif, bmp",
                          "error")
                    return redirect(url_for('auth.sign_up'))

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
            flash(error, "error")
        else:
            user_repo.update(username, name, email, img_id, hasher.hash(password))
            flash("User profile has been modified")
            return redirect(url_for('users.view_user', username=user.username))
    return render_template('auth/edit_required.html', user=user)
