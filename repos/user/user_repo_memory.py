"""Memory posts repo"""
import datetime
from flask import abort

from models.user import User
from .IUserRepo import IUserRepo

class RepoUserMemory(IUserRepo):
    """Repo for posts in memory"""
    def __init__(self, seed = None):
        if seed is None:
            self.users = []
        else:
            self.users = seed

    def get(self, username):
        """Returns post by id"""
        user = next((user for user in self.users if user.username == username), None)
        if user is not None:
            return user
        abort(404)

    def get_all(self):
        """Returns all posts"""
        return self.users

    def insert(self, user):
        """Add a new post"""
        if isinstance(user, User):
            self.users.append(user)

    def update(self, username, name, email, password):
        """Updates post by id"""
        user = self.get(username)
        if user is not None:
            user.name = name
            user.email = email
            user.password = password
            user.date_modified = datetime.datetime.now().strftime("%B %d %Y - %H:%M")

    def delete(self, username):
        """Deletes post by id"""
        for i, user in enumerate(self.users):
            if user.username == username:
                del self.users[i]
                break
