"""A class that holds posts so they can be operated on by routes in blueprints"""
from flask import current_app
from containers.repo_container import RepoContainer

class UserRepoHolder():
    """A class that holds posts so they can be operated on by routes in blueprints"""
    def __init__(self):
        self.users = None

    def create_repo(self):
        """Creates the repo"""
        db_type = current_app.config["DB_TYPE"]
        if db_type == 'db':
            self.users = RepoContainer().user_repo_db_factory()
        elif db_type == 'memory':
            self.users = RepoContainer().user_repo_memory_factory()
        elif db_type == 'alchemy':
            self.users = RepoContainer().user_repo_alchemy_factory()
        else:
            print('DB_TYPE not valid. Must be \'db\', \'alchemy\' or \'memory\'')

    def get(self):
        """Returns all posts"""
        if self.users is None:
            self.create_repo()
        return self.users
