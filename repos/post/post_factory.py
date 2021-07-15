"""Posts repo factory"""
from repos.post.post_repo_memory import RepoPostsMemory
from repos.post.post_repo_db import RepoPostsDB
from repos.post.seed import create_seed

class PostFactory():
    """Posts repo factory"""
    @staticmethod
    def create_repo(repo_type):
        """Creates repo from string"""
        if repo_type == "memory":
            return RepoPostsMemory(create_seed())
        if repo_type == "db":
            return RepoPostsDB(create_seed())
        print("Invalid type")
        return -1
