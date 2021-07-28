"""Class that handles authentication"""
from flask import flash, redirect, url_for, session
from werkzeug.security import generate_password_hash
from blueprints.users import users_repo
from models.user import User

class Authentication():
    """Class that handles authentication"""
    def __init__(self):
        pass

    def sign_up(self, username, name, email, password, confirm_password):
        """Signs user up"""
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

    def login(self, username, password):
        """Logs user in"""
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

    def logout(self):
        """Logs user out"""
        session.pop('username', None)
        flash("You are logged out")
