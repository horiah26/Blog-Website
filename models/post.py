"""Defines the Post class"""
import datetime

class Post:
    """Defines the post attributes"""
    def __init__(self, post_id, title, text, owner, date_created = None, date_modified = None):
        self.post_id = post_id
        self.title = title
        self.text = text
        self.owner = owner

        if date_created == None:
            self.date_created = datetime.datetime.now().strftime("%B %d %Y - %H:%M")
        else:
            self.date_created = date_created

        if date_modified == None:
            self.date_modified = datetime.datetime.now().strftime("%B %d %Y - %H:%M")
        else:
            self.date_modified = date_modified
