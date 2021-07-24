"""Blueprint for user management"""
from flask import (
    Blueprint, redirect, render_template, request, url_for, abort, flash, current_app, session, g
)
from flask_login import current_user, login_user, logout_user
from models.user import User
from models.user_repo_holder import UserRepoHolder
from blueprints.decorators.redirect_to_setup import redirect_to_setup
from blueprints.decorators.permission_required import permission_required

from werkzeug.security import generate_password_hash, check_password_hash

users_repo = UserRepoHolder()
bp = Blueprint('users', __name__)

@bp.route('/signup', methods=['GET', 'POST'])
@redirect_to_setup
def sign_up():
    """Creates a new user"""
    if request.method == 'POST':
        username = request.form['username'].strip()
        email = request.form['email'].strip()
        name = request.form['name'].strip()
        password = request.form['password'].strip()
        confirm_password = request.form['confirm_password'].strip()

        user = users_repo.get().get(username)

        error = None
        if user:
            error = "Username already taken"
        if user is not None and user.email == email:
            error = "Email adress already taken"
        if password != confirm_password:
            error = "Your password must match"
        if not password:
            error = "Password is required"
        if not confirm_password:
            error = "Please confirm your password"
        if not email:
            error = "Email is required"
        if not name:
            error = "Your name is required"
        if not username:
            error = "Username is required"
        if error is not None:
            flash(error)
        else:
            users_repo.get().insert(User(username, name, email, generate_password_hash(password)))  
            flash("You have signed up")
            return redirect(url_for('blog.home'))
    return render_template('users/sign_up.html')

@bp.route('/users', methods=['GET'])
@redirect_to_setup
def view_all():
    """Route to home"""
    return render_template('users/view_all.html', users = users_repo.get().get_all())

@bp.route('/users/<username>/', methods=['GET'])
@redirect_to_setup
def view_user(username):
    """Route to home"""
    if users_repo.get().get(username):
        return render_template('users/view.html', user = users_repo.get().get(username))
    abort(404)


@bp.route('/users/<username>/delete', methods=['GET'])
@redirect_to_setup
@permission_required()
def delete(username):
    """Route to home"""
    users_repo.get().delete(username)     
    flash("User deleted")
    return redirect(url_for('blog.home'))


@bp.route('/users/<username>/edit', methods=['GET', 'POST'])
@redirect_to_setup
@permission_required()
def edit(username):
    """Route to home"""
    user = users_repo.get().get(username)
    if user.username != current_user.username and current_user.username != 'admin':
        print('Only the User cand edit their post')
        return redirect(url_for('blog.home'))

    if request.method == 'POST':
        email = request.form['email'].strip()
        name = request.form['name'].strip()

        error = None
        if error is not None:
            print(error)                 
            flash(error)
        else:
            if not name:
                name = user.name
            elif not email:
                email = user.email
            else:
                users_repo.get().update(username, name, email, user.password)                     
                flash("User profile has been modified")
                return redirect(url_for('users.view_user', username = user.username))
    return render_template('users/edit.html', user = user)

@bp.route('/login', methods=['GET', 'POST'])
@redirect_to_setup
def login():
    """Creates a new user"""    
    if current_user.is_authenticated:
        return redirect(url_for('blog.home'))

    if request.method == 'POST':
        session.pop('username', None)

        username = request.form['username'].strip()
        password = request.form['password'].strip()

        user = users_repo.get().get(username)    
        if user is None or not user.check_password(password):
            flash('Invalid username or password')
            return redirect(url_for('users.login'))
        login_user(user)        
        flash("You are logged in")
        return redirect(url_for('blog.home'))
    return render_template('users/login.html')

@bp.route('/logout')
@redirect_to_setup
def logout():
    logout_user()     
    flash("You are logged out")
    return redirect(url_for('blog.home'))
