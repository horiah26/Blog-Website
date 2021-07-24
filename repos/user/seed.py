"""Seed data, posts for blog"""
from models.user import User
from werkzeug.security import generate_password_hash
user1 = User("username1", "Name 1", "email1@g.com", generate_password_hash("password1", method='pbkdf2:sha512:100'))
user2 = User("username2", "Name 2", "email2@g.com", generate_password_hash("password2", method='pbkdf2:sha512:100'))
user3 = User("username3", "Name 3", "email3@g.com", generate_password_hash("password3", method='pbkdf2:sha512:100'))
user4 = User("username4", "Name 4", "email4@g.com", generate_password_hash("password4", method='pbkdf2:sha512:100'))
admin = User("admin", "admin", "admin@g.com", generate_password_hash("admin", method='pbkdf2:sha512:100'))

def get():
    """Returns seed"""
    return [user1, user2, user3, user4, admin]
