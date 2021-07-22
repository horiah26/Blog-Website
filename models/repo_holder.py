"""A class that holds posts so they can be operated on by routes in blueprints"""
from flask import current_app, g
from repos.post.post_repo_factory import PostRepoFactory
from repos.user.user_repo_factory import UserRepoFactory

class RepoHolder():
    """A class that holds posts so they can be operated on by routes in blueprints"""
    def __init__(self):
        self.posts = None

    def create_repo(self):
        """Creates the repo"""
        db_type = current_app.config["DB_TYPE"]
        self.posts = PostRepoFactory.create_repo(db_type)

    def get(self):
        """Returns all posts"""
        if self.posts is None:
            self.create_repo()
        return self.posts
