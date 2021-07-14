"""Abstract class for posts repo"""
from abc import ABC, abstractmethod

class IPost (ABC):
    """Abstract class for posts repo"""
    @abstractmethod
    def get(self, post_id): pass

    @abstractmethod
    def get_all(self): pass

    @abstractmethod
    def update(self, post_id, title, text, date_modified): pass

    @abstractmethod
    def delete(self, post_id): pass
