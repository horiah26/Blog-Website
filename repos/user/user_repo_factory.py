"""Users repo factory"""
from repos.user.user_repo_memory import RepoUserMemory
from repos.user.user_repo_db import RepoUserDB
from repos.user import seed

class UserRepoFactory():
    """Posts repo factory"""
    @staticmethod
    def create_repo(repo_type):
        """Creates repo from string"""
        if repo_type == "memory":
            return RepoUserMemory(seed.get())        
        if repo_type == "db":
            return RepoUserDB(seed.get())
        print("Invalid factory type")
        return -1
