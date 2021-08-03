"""Seed data, posts for blog"""
from werkzeug.security import generate_password_hash
from containers.container import Container

container = Container()

user1 = container.user_factory("username1", "Name 1", "email1@g.com", generate_password_hash("password1", method='pbkdf2:sha512:100'))
user2 = container.user_factory("username2", "Name 2", "email2@g.com", generate_password_hash("password2", method='pbkdf2:sha512:100'))
user3 = container.user_factory("username3", "Name 3", "email3@g.com", generate_password_hash("password3", method='pbkdf2:sha512:100'))
user4 = container.user_factory("username4", "Name 4", "email4@g.com", generate_password_hash("password4", method='pbkdf2:sha512:100'))
admin = container.user_factory("admin", "admin", "admin@g.com", generate_password_hash("admin", method='pbkdf2:sha512:100'))

def get():
    """Returns seed"""
    return [user1, user2, user3, user4, admin]
