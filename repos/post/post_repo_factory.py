"""Posts repo factory"""
from repos.post.post_repo_memory import RepoPostsMemory
from repos.post.post_repo_db import RepoPostsDB
from repos.post import seed

from repos.user.user_repo_factory import UserRepoFactory

class PostRepoFactory():
    """Posts repo factory"""
    @staticmethod
    def create_repo(repo_type):
        """Creates repo from string"""
        UserRepoFactory().create_repo(repo_type)
        if repo_type == "memory":
            return RepoPostsMemory(seed.get())
        if repo_type == "db":
            return RepoPostsDB(seed.get())
        print("Invalid type")
        return -1
