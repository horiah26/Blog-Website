"""Handles post statistics"""

from datetime import datetime
from dependency_injector.wiring import inject, Provide
from collections import Counter

class Statistics():
    """Handles post statistics"""
    def __init__(self, post_repo = Provide['post_repo'], auth = Provide['auth']):
        self.posts = post_repo.get_all()
        self.auth = auth

    def get(self):
        dates = []
        for post in self.posts:
            if self.auth.logged_user() == post.owner or self.auth.logged_user() == 'admin':
                date = datetime.strptime(post.date.created, "%B %d %Y - %H:%M").date()
                time = str(date.year) + "-" + str(date.month)
                dates.append(time)
        sorted_dates = sorted(dates, key=None, reverse=True)
        return dict(Counter(sorted_dates))
