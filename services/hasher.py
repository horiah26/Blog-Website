"""Handles password hashing"""
from werkzeug.security import generate_password_hash, check_password_hash

from models.user import User


class Hasher():
    """Handles password hashing"""

    def __init__(self):
        pass

    def hash(self, password):
        """Returns password hash"""
        return generate_password_hash(password, method='pbkdf2:sha512:100')

    def check_password(self, user: User, password):
        """Checks hashed password"""
        return check_password_hash(user.password, password)
