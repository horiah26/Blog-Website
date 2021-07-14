"""Abstract class for posts repo"""
from abc import ABC, abstractmethod

class IPost (ABC):
    """Abstract class for posts repo"""
    @abstractmethod
    def get(self, id): pass

    @abstractmethod
    def get_all(self): pass

    @abstractmethod
    def update(self, id, title, text, date_modified): pass

    @abstractmethod
    def delete(self, id): pass
