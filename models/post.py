"""Defines the Post class"""

from models.date import Date

class Post:
    """Defines the post attributes"""
    def __init__(self, post_id, title, text, owner, img_id, date = Date()):
        self.post_id = post_id
        self.title = title
        self.text = text
        self.owner = owner
        self.img_id = img_id
        self.date = date
