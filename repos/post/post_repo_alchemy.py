"""SQLAlchemy repo"""

import datetime
import math
from static import constant

from sqlalchemy.sql import func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.alchemy_url import AlchURL

from dependency_injector.wiring import inject, Provide
from containers.container import Container
from .IPostRepo import IPostRepo

db_string = AlchURL().get_url()
db = create_engine(db_string)
base = declarative_base()

Session = sessionmaker(db)
session = Session()

Base = automap_base()
Base.prepare(db, reflect=True)
Post = Base.classes.posts
User = Base.classes.users

container = Container()

class RepoPostsAlchemy(IPostRepo):
    """SQLAlchemy repo"""
    def __init__(self, seed = None):
        """Initializes class and adds posts from seed if present"""
        if seed is not None and self.get_all() is not None and len(self.get_all()) == 0:
            print(len(self.get_all()))
            for post in seed:
                self.insert(post)

    def insert(self, post):
        """Add a new post"""
        new_post = Post(post_id = post.post_id, title = post.title, text = post.text, owner = post.owner, date_created = post.date_created, date_modified = post.date_modified)
        session.add(new_post)
        session.commit()

    def get(self, post_id):
        """Returns post by id"""
        post = session.query(Post.post_id, Post.title, Post.text, Post.owner, Post.date_created, Post.date_modified, User.name).join(User, User.username == Post.owner).filter(Post.post_id == post_id).first()
        return (container.post_factory(post[0], post[1], post[2], post[3], post[4], post[5]), post[6])

    def get_all(self):
        """Returns all posts"""
        return session.query(Post).all()

    def update(self, post_id, title, text):
        """Updates post by id"""
        post = session.query(Post).filter(Post.post_id == post_id).first()
        post.title = title
        post.text = text
        post.date_modified = datetime.datetime.now().strftime("%B %d %Y - %H:%M")
        session.commit()

    def delete(self, post_id):
        """Deletes post by id"""
        post = session.query(Post).filter(Post.post_id == post_id).first()
        session.delete(post)
        session.commit()

    def get_previews(self, username = None, per_page = 6, page_num = 1):
        """Returns previews of posts posts"""
        offset_nr = (page_num - 1) * per_page
        previews = []
        if username:
            for post_id, title, prev_text, name, username, date_created, date_modified in session.query(Post.post_id, Post.title, func.substr(Post.text, 0, constant.PREVIEW_LENGTH), User.name, Post.owner, Post.date_created, Post.date_modified).join(User, User.username == Post.owner).filter(User.username == username).order_by(Post.post_id.desc()).slice(offset_nr, offset_nr + per_page):
                previews.append(container.preview_factory(post_id, title, prev_text, name, username, date_created, date_modified))
        else:
            for post_id, title, prev_text, name, username, date_created, date_modified in session.query(Post.post_id, Post.title, func.substr(Post.text, 0, constant.PREVIEW_LENGTH), User.name, Post.owner, Post.date_created, Post.date_modified).join(User, User.username == Post.owner).order_by(Post.post_id.desc()).limit(per_page).offset(offset_nr):
                previews.append(container.preview_factory(post_id, title, prev_text, name, username, date_created, date_modified))
     
                        
        if username:
            total_posts = session.query(Post.post_id).filter(Post.owner == username).count()
        else:
            total_posts = session.query(Post.post_id).count()
            
        total_pages = math.ceil(total_posts / per_page)
        return (previews, total_pages)

    def next_id(self):
        """Returns next id"""
        return session.query(func.max(Post.post_id)).first()[0] + 1
