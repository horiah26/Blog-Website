"""Hashes the passwords of users imported from a database with posts"""
from werkzeug.security import generate_password_hash
from containers.repo_container import RepoContainer

class HashImportedPasswords():
    """Hashes the passwords of users imported from a database with posts"""
    def __init__(self):
        self.repo = RepoContainer().user_repo_db_factory()

    def hash(self):
        """Hashes the passwords of users imported from a database with posts"""
        users = self.repo.get_all()
        for user in users:
            if user.password == user.username:
                self.repo.update(user.username, user.name, user.email, generate_password_hash(user.password, method='pbkdf2:sha512:100'))
