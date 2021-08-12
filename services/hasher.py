
from werkzeug.security import generate_password_hash, check_password_hash
from dependency_injector.wiring import inject, Provide

from models.user import User

class Hasher():
    def __init__(self):
        pass

    def hash(self, password):
        """Hashes password"""
        return generate_password_hash(password, method='pbkdf2:sha512:100')
    
    def check_password(self, user : User, password):
        """Checks hassed password"""
        return check_password_hash(user.password, password)
