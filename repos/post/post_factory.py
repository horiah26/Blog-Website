"""Posts repo factory"""
from repos.post.post_repo_memory import RepoPosts
from repos.post.seed import create_seed

class PostFactory():
    """Posts repo factory"""
    @staticmethod
    def create_repo(repo_type):
        """Creates repo from string"""
        if repo_type == "memory":
            return RepoPosts(create_seed())
        if repo_type == "db":
            return RepoPosts(create_seed())
        print("Invalid type")
        return -1
