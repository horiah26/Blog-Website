"""Memory posts repo"""
from datetime import datetime
from dependency_injector.wiring import inject, Provide
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
        if user:
            return user

    def get_all(self):
        """Returns all posts"""
        return self.users

    def insert(self, user):
        """Add a new post"""
        if isinstance(user, User):
            self.users.append(user)

    def update(self, username, name, email, img_id, password):
        """Updates post by id"""
        user = self.get(username)
        if user is not None:
            user.name = name
            user.email = email
            user.password = password
            user.img_id = img_id
            user.date_modified = datetime.now().strftime("%B %d %Y - %H:%M")

    def delete(self, username):
        """Deletes post by id"""
        for i, user in enumerate(self.users):
            if user.username == username:
                del self.users[i]
                break
    @inject
    def get_users_with_posts(self, post_repo = Provide['post_repo']):
        """Returns all users that have at least one active post"""
        posts = post_repo.get_all()
        users_with_posts = []
        for user in self.users:
            for post in posts:
                if user.username == post.owner:
                    users_with_posts.append(user)

        return list(set(users_with_posts))
