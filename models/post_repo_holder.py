"""A class that holds posts so they can be operated on by routes in blueprints"""
from flask import current_app
from dependency_injector.wiring import inject, Provide

class PostRepoHolder():
    """A class that holds posts so they can be operated on by routes in blueprints"""
    def __init__(self):
        self.posts = None
    @inject
    def create_repo(self, post_repo_db = Provide['post_repo_db'],
                    post_repo_memory = Provide['post_repo_memory'],
                    post_repo_alchemy = Provide['post_repo_alchemy']):
        """Creates the repo"""
        db_type = current_app.config["DB_TYPE"]
        if db_type == 'db':
            self.posts = post_repo_db
        elif db_type == 'memory':
            self.posts = post_repo_memory
        elif db_type == 'alchemy':
            self.posts = post_repo_alchemy

        else:
            print('DB_TYPE not valid. Must be \'db\', \'alchemy\' or \'memory\'')

    def get(self):
        """Returns all posts"""
        if self.posts is None:
            self.create_repo()
        return self.posts
