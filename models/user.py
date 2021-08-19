"""The user class"""

from models.date import Date

class User():
    """The user class"""
    def __init__(self, username, name, email, password, date = Date()):
        self.username = username
        self.name = name
        self.email = email
        self.password = password        
        self.date = date

    def get(self, username):
        """Returns this post"""
        if self.username == username:
            return self
        return None
