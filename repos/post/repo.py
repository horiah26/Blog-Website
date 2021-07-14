"""Memory posts repo """
from flask import abort

from models.post import Post
from .IPost import IPost

class RepoPosts(IPost):
    """Returns post by id"""
    def __init__(self, seed):
        self.posts = seed

    def get(self, id):
        """Returns post by id"""
        post = next((post for post in self.posts if post.id == id), None)
        if post is not None:
            return post
        else:
            abort(404)

    def get_all(self):
        """Returns all posts"""
        return self.posts

    def insert(self, post):
        """Add a new post"""
        if isinstance(post, Post):
            self.posts.append(post)

    def update(self, id, title, text, date_modified):
        """Updates post by id"""
        post = self.get(id)
        post.title = title
        post.text = text
        post.date_modified = date_modified

    def delete(self, id):
        """Deletes post by id"""
        for i, post in enumerate(self.posts):
            if post.id == id:
                del self.posts[i]
                break

    def next_id(self):
        """Returns available id for new post"""
        if len(self.posts) == 0:
            id = 1
        else:
            id = max(post.id for post in self.posts) + 1
        return id
