"""Class that handles creation and modification date for posts and users"""
import datetime

class Date:
    """Class that handles creation and modification date for posts and users"""
    def __init__(self, created = None, modified = None):
        if created is None and modified is None:
            self.created = datetime.datetime.now().strftime("%B %d %Y - %H:%M")
            self.modified = datetime.datetime.now().strftime("%B %d %Y - %H:%M")
        elif created is not None and modified is None:
            self.created = created
            self.modified = created
        else:
            self.created = created
            self.modified = modified
