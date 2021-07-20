"""Users repo factory"""
from repos.user.user_repo_memory import RepoUserMemory
from repos.user.user_repo_db import RepoUserDB

class UserRepoFactory():
    """Posts repo factory"""
    @staticmethod
    def create_repo(repo_type, seed = None):
        """Creates repo from string"""
        if repo_type == "memory":
            return RepoUserMemory(seed)
        if repo_type == "db":
            return RepoUserDB(seed)
        print("Invalid factory type")
        return -1
