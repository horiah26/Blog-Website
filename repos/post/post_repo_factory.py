"""Posts repo factory"""
from repos.post.post_repo_memory import RepoPostsMemory
from repos.post.post_repo_db import RepoPostsDB

class PostRepoFactory():
    """Posts repo factory"""
    @staticmethod
    def create_repo(repo_type, seed = None):
        """Creates repo from string"""
        if repo_type == "memory":
            return RepoPostsMemory(seed)
        if repo_type == "db":
            return RepoPostsDB(seed)
        print("Invalid type")
        return -1
