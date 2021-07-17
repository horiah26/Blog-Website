"""A class that holds posts so they can be operated on by routes in blueprints"""
from repos.post.post_factory import PostFactory

class RepoHolder():
    """A class that holds posts so they can be operated on by routes in blueprints"""
    def __init__(self):
        self.posts = None

    def create_repo(self, app):
        db_type = app.config["DB_TYPE"]
        self.posts = PostFactory.create_repo(db_type)