"""Blueprint for authentication management"""
from flask import (
    Blueprint, redirect, render_template, request, url_for, session, flash
)
from dependency_injector.wiring import inject, Provide
from blueprints.decorators.redirect_to_setup import redirect_to_setup

bp = Blueprint('auth', __name__)


@bp.route('/signup', methods=['GET', 'POST'])
@redirect_to_setup
@inject
def sign_up(auth=Provide['auth'], user_img=Provide['profile_img_repo']):
    """Creates a new user"""
    img_id = 0
    if request.method == 'POST':
        username = request.form['username'].strip()
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

        return auth.sign_up(username, name, email, password, confirm_password, img_id)
    return render_template('auth/sign_up.html')


@bp.route('/login', methods=['GET', 'POST'])
@redirect_to_setup
@inject
def login(auth=Provide['auth']):
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
def logout(auth=Provide['auth']):
    """Log out user"""
    auth.logout()
    return redirect(url_for('blog.home'))
