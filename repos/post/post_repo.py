from flask import abort

from .abstract_post import AbstractRepoPosts
from .seed import seed
from models.post import Post

class RepoPosts(AbstractRepoPosts):
    def __init__(self, seed):
        self.posts = seed

    def get(self, id):
            post = next((post for post in self.posts if post.id == id), None)
            if post is not None:
                return post
            else:
                abort(404)

    def get_all(self):
        return self.posts

    def add(self, post):
        if isinstance(post, Post):
            self.posts.append(post)

    def update(self, id, title, text, date_modified):
        post = self.get(id)
        post.title = title
        post.text = text
        post.date_modified = date_modified

    def delete(self, id):
        for i, post in enumerate(self.posts):
            if post.id == id:
                del self.posts[i]
                break            

    def next_id(self): 
        if(len(self.posts) == 0):
            id = 1
        else:                
            id = max(post.id for post in self.posts) + 1 
        return id


repo_posts = RepoPosts(seed)