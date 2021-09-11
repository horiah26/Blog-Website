"""Defines the Post class"""

from models.date import Date


class Post:
    """Defines the post attributes"""

    def __init__(self, post_id, title, text, owner, img_id, date=Date()):
        self.post_id = post_id
        self.title = title
        self.text = text
        self.owner = owner
        self.img_id = img_id
        self.date = date

    def get_dict(self):
        """Returns instance of Post as dictionary"""
        return {'post_id': self.post_id,
                'title': self.title,
                'text': self.text,
                'owner': self.owner,
                'img_id': self.img_id,
                'date_created': self.date.created,
                'date_modified': self.date.modified
                }
