"""Abstract class for posts repo"""
from abc import ABC, abstractmethod

class IPostRepo (ABC):
    """Abstract class for posts repo"""
    @abstractmethod
    def get(self, post_id):
        """Get post by id"""

    @abstractmethod
    def get_all(self):
        """Get all posts"""

    @abstractmethod
    def insert(self, post):
        "Insert post"

    @abstractmethod
    def update(self, post_id, title, text, img_id):
        """Update post"""

    @abstractmethod
    def delete(self, post_id):
        """Delete post"""

    @abstractmethod
    def get_previews(self, username = None, per_page = 6, page_num = 1):
        """Returns preview of all posts"""
