"""Abstract class for users repo"""
from abc import ABC, abstractmethod

class IUserRepo (ABC):
    """Abstract class for users repo"""
    @abstractmethod
    def get(self, username):
        """Get user by id"""

    @abstractmethod
    def get_all(self):
        """Get all users"""

    @abstractmethod
    def insert(self, user):
        """Add user"""

    @abstractmethod
    def update(self, username, name, email, password):
        """Update user"""

    @abstractmethod
    def delete(self, username):
        """Delete user"""

    @abstractmethod
    def get_users_with_posts(self):
        """Return users with posts"""
