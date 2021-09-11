"""Class that handles authentication"""
from flask import flash, redirect, url_for, session
from dependency_injector.wiring import inject, Provide
from models.user import User


class Authentication:
    """Class that handles authentication"""

    def __init__(self, user_repo):
        self.user_repo = user_repo

    def sign_up(self, username, name, email, password, confirm_password, img_id, hasher=Provide['hasher']):
        """Signs user up"""

        user = self.user_repo.get(username)
        users = self.user_repo.get_all()

        email_taken = False
        for item in users:
            if item.email == email:
                email_taken = True
                break

        error = None
        if user:
            error = "Username is already in use"
        if email_taken:
            error = "Email adress is already in use"
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
            flash(error, "error")
            return redirect(url_for('auth.sign_up'))
        self.user_repo.insert(User(username, name, email, hasher.hash(password), img_id))
        flash("You have signed up")
        return redirect(url_for('blog.home'))

    @inject
    def login(self, username, password, hasher=Provide['hasher']):
        """Logs user in"""
        user = self.user_repo.get(username)
        if user is None or not hasher.check_password(user, password):
            flash('Invalid username or password', "error")
            return redirect(url_for('auth.login'))
        session['username'] = user.username
        if '@temporary.com' in user.email:
            flash('This user has been imported and must be updated', "error")
            return redirect(url_for('users.edit_required', username=user.username))
        flash("You are logged in")
        return redirect(url_for('blog.home'))

    def logout(self):
        """Logs user out"""
        session.pop('username', None)
        flash("You are logged out")

    def logged_user(self):
        """If any user is logged in return true, else return false"""
        if 'username' in session:
            return session['username']
        return False
