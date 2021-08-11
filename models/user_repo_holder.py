"""A class that holds posts so they can be operated on by routes in blueprints"""
from flask import current_app
from dependency_injector.wiring import inject, Provide

class UserRepoHolder():
    """A class that holds posts so they can be operated on by routes in blueprints"""
    def __init__(self):
        self.users = None

    def create_repo(self, user_repo_db = Provide['user_repo_db'],
                    user_repo_memory = Provide['user_repo_memory'],
                    user_repo_alchemy = Provide['user_repo_alchemy']):
        """Creates the repo"""
        db_type = current_app.config["DB_TYPE"]
        if db_type == 'db':
            self.users = user_repo_db
        elif db_type == 'memory':
            self.users = user_repo_memory
        elif db_type == 'alchemy':
            self.users = user_repo_alchemy
        else:
            print('DB_TYPE not valid. Must be \'db\', \'alchemy\' or \'memory\'')

    def get(self):
        """Returns all posts"""
        if self.users is None:
            self.create_repo()
        return self.users
