"""Blueprint for user management"""
from flask import (
    Blueprint, redirect, render_template, request, url_for, current_app, session, g
)
from flask_login import current_user, login_user, logout_user
from models.user import User
from repos.user.user_repo_factory import UserRepoFactory
from blueprints.decorators.redirect_to_setup import redirect_to_setup

factory = UserRepoFactory()
users_repo = factory.create_repo('db')
bp = Blueprint('users', __name__)

@bp.route('/signup', methods=['GET', 'POST'])
@redirect_to_setup()
def sign_up():
    """Creates a new user"""
    if request.method == 'POST':
        username = request.form['username'].strip()
        email = request.form['email'].strip()
        name = request.form['name'].strip()
        password = request.form['password'].strip()
        confirm_password = request.form['confirm_password'].strip()

        error = None
        if not username:
            error = "Username is required"
        if not email:
            error = "Email is required"
        if not "@" in email or not "." in email:
            error = "Email is invalid"
        if not name:
            error = "Your name is required"
        if not password:
            error = "Password is required"
        if not confirm_password:
            error = "Please confirm your password"
        if password != confirm_password:
            error = "Your password must match"
        if error is not None:
            print(error)
        else:
            users_repo.insert(User(username, name, email, password))
            return redirect(url_for('blog.home'))
    return render_template('users/sign_up.html')

@bp.route('/users', methods=['GET'])
@redirect_to_setup()
def view_all():
    """Route to home"""
    return render_template('users/view_all.html', users = users_repo.get_all())

@bp.route('/users/<username>/', methods=['GET'])
@redirect_to_setup()
def view_user(username):
    """Route to home"""
    return render_template('users/view.html', user = users_repo.get(username))

@bp.route('/users/<username>/delete', methods=['GET'])
@redirect_to_setup()
def delete(username):
    """Route to home"""
    users_repo.delete(username)
    return redirect(url_for('blog.home'))


@bp.route('/users/<username>/edit', methods=['GET', 'POST'])
@redirect_to_setup()
def edit(username):
    """Route to home"""
    user = users_repo.get(username)
    if request.method == 'POST':
        email = request.form['email'].strip()
        name = request.form['name'].strip()

        error = None
        #if not "@" in email or not "." in email:
        #    error = "Email is invalid"
        if error is not None:
            print(error)
        else:
            if not name:
                name = user.name
            elif not email:
                email = user.email
            else:
                users_repo.update(username, name, email, user.password)
                return redirect(url_for('users.view_user', username = user.username))
    return render_template('users/edit.html', user = user)

@bp.route('/login', methods=['GET', 'POST'])
@redirect_to_setup()
def login():
    """Creates a new user"""    
    if current_user.is_authenticated:
        return redirect(url_for('blog.home'))

    if request.method == 'POST':
        session.pop('username', None)

        username = request.form['username'].strip()
        password = request.form['password'].strip()

        user = users_repo.get(username)
        print(user)
        if user is None or not user.check_password(password):
            print('Invalid username or password')
            return redirect(url_for('users.login'))
        login_user(user, remember=True)
        return redirect(url_for('blog.home'))
    return render_template('users/login.html')

@bp.route('/logout')
@redirect_to_setup()
def logout():
    logout_user()
    return redirect(url_for('blog.home'))
