"""Blueprint for authentication management"""
from flask import (
    Blueprint, redirect, render_template, request, url_for, session
)
from blueprints.decorators.redirect_to_setup import redirect_to_setup
from database.authentication import Authentication

bp = Blueprint('auth', __name__)
auth_service = Authentication()

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

        return auth_service.sign_up(username, name, email, password, confirm_password)
    return render_template('auth/sign_up.html')

@bp.route('/login', methods=['GET', 'POST'])
@redirect_to_setup
def login():
    """Log in user"""
    if request.method == 'POST':
        session.pop('username', None)

        username = request.form['username'].strip()
        password = request.form['password'].strip()

        return auth_service.login(username, password)

    return render_template('auth/login.html')

@bp.route('/logout', methods=['GET', 'POST'])
@redirect_to_setup
def logout():
    """Log out user"""
    auth_service.logout()
    return redirect(url_for('blog.home'))
