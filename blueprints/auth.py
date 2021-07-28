"""Blueprint for authentication management"""
from flask import (
    Blueprint, redirect, render_template, request, url_for, flash, session
)
from werkzeug.security import generate_password_hash
from models.user import User
from blueprints.decorators.redirect_to_setup import redirect_to_setup
from blueprints.decorators.create_tables import create_tables
from .users import users_repo

bp = Blueprint('auth', __name__)

@bp.route('/signup', methods=['GET', 'POST'])
@redirect_to_setup
@create_tables
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
            users_repo.get().insert(User(username, name, email, generate_password_hash(password, method='pbkdf2:sha512:100')))
            flash("You have signed up")
            return redirect(url_for('blog.home'))
    return render_template('auth/sign_up.html')

@bp.route('/login', methods=['GET', 'POST'])
@redirect_to_setup
@create_tables
def login():
    """Log in user"""
    if request.method == 'POST':
        session.pop('username', None)

        username = request.form['username'].strip()
        password = request.form['password'].strip()

        user = users_repo.get().get(username)
        if user is None or not user.check_password(password):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        session['username'] = user.username
        if '@temporary.com' in user.email:
            flash('This user has been imported and must be updated')
            return redirect(url_for('users.edit_required', username = user.username))
        flash("You are logged in")
        return redirect(url_for('blog.home'))
    return render_template('auth/login.html')

@bp.route('/logout', methods=['GET', 'POST'])
@redirect_to_setup
@create_tables
def logout():
    """Log out user"""
    session.pop('username', None)
    flash("You are logged out")
    return redirect(url_for('blog.home'))
