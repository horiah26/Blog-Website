"""Blueprint for user management"""
from flask import (
    Blueprint, redirect, render_template, request, url_for, flash, session
)
from werkzeug.security import generate_password_hash
from models.user_repo_holder import UserRepoHolder
from blueprints.decorators.redirect_to_setup import redirect_to_setup
from blueprints.decorators.permission_required import permission_required
from blueprints.decorators.create_tables import create_tables

users_repo = UserRepoHolder()
bp = Blueprint('users', __name__)

@bp.route('/users', methods=['GET'])
@redirect_to_setup
@create_tables
def view_all():
    """View all users"""
    return render_template('users/view_all.html', users = users_repo.get().get_all())

@bp.route('/users/<username>/', methods=['GET'])
@redirect_to_setup
@create_tables
def view_user(username):
    """View user"""
    if users_repo.get().get(username):
        return render_template('users/view.html', user = users_repo.get().get(username))
    flash('User not found')
    return redirect(url_for('users.view_all'))

@bp.route('/users/<username>/delete', methods=['GET'])
@redirect_to_setup
@permission_required()
@create_tables
def delete(username):
    """Delete user"""
    try:
        users_repo.get().delete(username)
        flash("User deleted")
    except Exception:
        flash("Delete user's posts first")
    return redirect(url_for('blog.home'))

@bp.route('/users/<username>/edit', methods=['GET', 'POST'])
@redirect_to_setup
@permission_required()
@create_tables
def edit(username):
    """Edit user"""
    user = users_repo.get().get(username)
    if user.username != session['username'] and session['username'] != 'admin':
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
                print("Here3")
            flash("User profile has been modified")
            return redirect(url_for('users.view_user', username = user.username))
    return render_template('auth/edit.html', user = user)

@bp.route('/users/<username>/edit_required', methods=['GET', 'POST'])
@redirect_to_setup
@permission_required()
def edit_required(username):
    """Edit user"""
    user = users_repo.get().get(username)
    if user.username != session['username'] and session['username'] != 'admin':
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
