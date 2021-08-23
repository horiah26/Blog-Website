"""Seed data, posts for blog"""

from models.user import User
from services.hasher import Hasher

def get():
    """Returns seed"""
    hasher = Hasher()

    user1 = User("username1", "Name 1", "email1@g.com", hasher.hash("password1"), 0)
    user2 = User("username2", "Name 2", "email2@g.com", hasher.hash("password2"), 0)
    user3 = User("username3", "Name 3", "email3@g.com", hasher.hash("password3"), 0)
    user4 = User("username4", "Name 4", "email4@g.com", hasher.hash("password4"), 0)
    admin = User("admin", "admin", "admin@g.com", hasher.hash("admin"), 0)

    return [user1, user2, user3, user4, admin]
