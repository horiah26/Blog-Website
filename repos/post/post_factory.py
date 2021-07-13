from repos.post.repo import RepoPosts
from repos.post.seed import create_seed

class PostFactory():
	@staticmethod
	def create_repo(type):
		if type == "memory":
			return RepoPosts(create_seed())
		if type == "db":
			return RepoPosts(create_seed())
		print("Invalid type")
		return -1
		
