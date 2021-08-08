"""SQLAlchemy repo"""
import datetime
import psycopg2
from flask import current_app
from static import constant
from .IUserRepo import IUserRepo

from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine  
from sqlalchemy import Column, String  
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker
from config.alchemy_url import AlchURL

from containers.container import Container
from containers.db_container import DBContainer

db_string = AlchURL().get_url()
db = create_engine(db_string)  
base = declarative_base()

Session = sessionmaker(db)  
session = Session()

Base = automap_base()
Base.prepare(db, reflect=True)
User = Base.classes.users

container = Container()
class RepoUserAlchemy(IUserRepo):
    def __init__(self, seed = None):
        """Initializes class and adds users from seed if present"""
        if seed is not None and self.get_all() is not None and len(self.get_all()) == 0:
            for post in seed:
                self.insert(post)

    def insert(self, user):
        """Add a new user"""
        new_user = User(username = user.username, name = user.name, email = user.email, password = user.password, date_created = user.date_created, date_modified = user.date_modified)
        session.add(new_user)         
        session.commit()

    def get(self, username):
        """Returns user by id"""
        user = session.query(User).get(username)
        if user is None:
            return None
        return container.user_factory(user.username, user.name, user.email, user.password, user.date_created, user.date_modified)
        
    def get_all(self):
        """Returns all users"""
        users = []
        query = session.query(User).all()
        for user in query:
            users.append(container.user_factory(user.username, user.name, user.email, user.password, user.date_created, user.date_modified))
        return users

    def update(self, username, name, email, password): 
        """Updates user by id"""
        user = session.query(User).filter(User.username == username).one()
        user.username = username
        user.name = name
        user.email = email
        user.password = password
        session.commit()

    def delete(self, username):
        """Deletes user by id"""  
        user = session.query(User).filter(User.username == username).one()
        session.delete(user)
        session.commit()
