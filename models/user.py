"""The user class"""

from models.date import Date

class User():
    """The user class"""
    def __init__(self, username, name, email, password, img_id, date = Date()):
        self.username = username
        self.name = name
        self.email = email
        self.password = password
        self.img_id = img_id
        self.date = date
