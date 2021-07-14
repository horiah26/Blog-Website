from repos.db import repo
from models.post import Post
from repos.db import erase
erase.erase_all_posts()

repo.insert(Post(1, "titlu1", "text1","proprietar1", "azi1", "ieri1"))
repo.insert(Post(2, "titlu2", "text2","proprietar2", "azi2", "ieri2"))
repo.insert(Post(3, "titlu3", "text3","proprietar3", "azi3", "ieri3"))

print(repo.get_all())