"""Creates tables"""
import psycopg2
from repos.post import seed as post_seed
from repos.user import seed as user_seed

from database.connection import Connection

from repos.post.post_repo_factory import PostRepoFactory
from repos.user.user_repo_factory import UserRepoFactory

class SeedTables():
    """Seeds the tables"""
    def __init__(self, app):
        self.DB_TYPE = app.config['DB_TYPE']

    def seed_all(self):
        """Seeds all tables in proper order"""  
        self.seed_users()
        self.seed_posts()

    def seed_users(self):
        """Seeds the users table"""  
        user_repo_factory = UserRepoFactory()
        user_repo_factory.create_repo(self.DB_TYPE, user_seed.get())

    def seed_posts(self):
        """Seeds the posts table"""  
        post_repo_factory = PostRepoFactory()
        post_repo_factory.create_repo(self.DB_TYPE, post_seed.get())