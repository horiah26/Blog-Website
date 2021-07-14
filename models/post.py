"""Defines the Post class"""
import datetime

class Post:
    """Defines the post attributes"""
    def __init__(self, post_id, title, text, owner):
        self.post_id = post_id
        self.title = title
        self.text = text
        self.date_created = datetime.datetime.now().strftime("%B %d %Y %H:%M")
        self.date_modified = datetime.datetime.now().strftime("%B %d %Y %H:%M")
        self.owner = owner
