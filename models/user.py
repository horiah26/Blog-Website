"""The user class"""
import datetime

class User():
    """The user class"""
    def __init__(self, username, name, email, password, date_created = None, date_modified = None):
        self.username = username
        self.name = name
        self.email = email
        self.password = password

        if date_created is None:
            self.date_created = datetime.datetime.now().strftime("%B %d %Y - %H:%M")
        else:
            self.date_created = date_created

        if date_modified is None:
            self.date_modified = datetime.datetime.now().strftime("%B %d %Y - %H:%M")
        else:
            self.date_modified = date_modified

    def __repr__(self):
        return f'<User: {self.username}>'


    def get(self, username):
        """Returns this post"""
        if self.username == username:
            return self
        return None
