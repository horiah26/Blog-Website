"""Blueprint for authentication management"""
from flask import (
    Blueprint, redirect, render_template, request, url_for, session
)
from dependency_injector.wiring import inject, Provide
from blueprints.decorators.redirect_to_setup import redirect_to_setup

bp = Blueprint('auth', __name__)

@bp.route('/signup', methods=['GET', 'POST'])
@redirect_to_setup
@inject
def sign_up(auth = Provide['auth']):
    """Creates a new user"""
    if request.method == 'POST':
        username = request.form['username'].strip()
        email = request.form['email'].strip()
        name = request.form['name'].strip()
        password = request.form['password'].strip()
        confirm_password = request.form['confirm_password'].strip()

        return auth.sign_up(username, name, email, password, confirm_password)
    return render_template('auth/sign_up.html')

@bp.route('/login', methods=['GET', 'POST'])
@redirect_to_setup
@inject
def login(auth = Provide['auth']):
    """Log in user"""
    if request.method == 'POST':
        session.pop('username', None)

        username = request.form['username'].strip()
        password = request.form['password'].strip()

        return auth.login(username, password)

    return render_template('auth/login.html')

@bp.route('/logout', methods=['GET', 'POST'])
@redirect_to_setup
@inject
def logout(auth = Provide['auth']):
    """Log out user"""
    auth.logout()
    return redirect(url_for('blog.home'))
