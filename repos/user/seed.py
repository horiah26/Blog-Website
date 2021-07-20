"""Seed data, posts for blog"""
from models.user import User

user1 = User("username1", "Name 1", "email1@g.com", "password1")
user2 = User("username2", "Name 2", "email2@g.com", "password2")
user3 = User("username3", "Name 3", "email3@g.com", "password3")
user4 = User("username4", "Name 4", "email4@g.com", "password4")

def get():
    """Returns seed"""
    return [user1, user2, user3, user4]
