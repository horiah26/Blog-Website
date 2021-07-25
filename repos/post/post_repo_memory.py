"""Memory posts repo """
import datetime
from flask import abort

from models.post import Post
from models.post_preview import PostPreview
from static import constant
from .IPostRepo import IPostRepo
from repos.user.user_repo_factory import UserRepoFactory

class RepoPostsMemory(IPostRepo):
    """Repos for posts in memory"""
    def __init__(self, seed):
        self.posts = seed

    def get(self, post_id):
        """Returns post by id"""
        post = next((post for post in self.posts if post.post_id == post_id), None)
        if post is not None:
            return post
        abort(404)

    def get_all(self):
        """Returns all posts"""
        return self.posts

    def insert(self, post):
        """Add a new post"""
        if isinstance(post, Post):
            self.posts.append(post)

    def update(self, post_id, title, text):
        """Updates post by id"""
        post = self.get(post_id)
        post.title = title
        post.text = text
        post.date_modified = datetime.datetime.now().strftime("%B %d %Y - %H:%M")

    def delete(self, post_id):
        """Deletes post by id"""
        for i, post in enumerate(self.posts):
            if post.post_id == post_id:
                del self.posts[i]
                break

    def next_id(self):
        """Returns available id for new post"""
        if len(self.posts) == 0:
            post_id = 1
        else:
            post_id = max(post.post_id for post in self.posts) + 1
        return post_id

    def get_previews(self):
        """Returns previews of posts posts"""
        posts = self.get_all()
        previewed_posts = []
        users = UserRepoFactory().create_repo('memory').get_all()
        for post in posts:            
            for user in users:
                if post.owner == user.username:
                    previewed_posts.append(PostPreview(post.post_id, post.title, post.text[0:constant.PREVIEW_LENGTH], user.name, post.date_created, post.date_modified))
                    break
        return previewed_posts
