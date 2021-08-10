from sqlalchemy.sql import func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.alchemy_url import AlchURL
from config.config_db import ConfigDB

from containers.container import Container
container = Container()

class AlchSession():
    def __init__(self):
        self.db_string = AlchURL().get_url()
        self.db = create_engine(self.db_string)
        self.base = declarative_base()

        Session = sessionmaker(self.db)
        self.session = Session()

        self.Base = automap_base()
        self.Base.prepare(self.db, reflect=True)
        self.Post = self.Base.classes.posts
        self.User = self.Base.classes.users

    def add(self, newpost):
        self.session.add(new_post)        
        session.commit()

    def get_post(self, post_id):
        post = self.session.query(self.Post.post_id, self.Post.title, self.Post.text, self.Post.owner, self.Post.date_created, self.Post.date_modified, self.User.name).join(self.User, self.User.username == self.Post.owner).filter(self.Post.post_id == post_id).first()
        return (container.post_factory(post[0], post[1], post[2], post[3], post[4], post[5]), post[6])

    def get_all_posts(self):
        return self.session.query(self.Post).all()

    def get_previews(self, username = None):
        previews = []
        if username:
            for post_id, title, prev_text, name, username, date_created, date_modified in self.session.query(self.Post.post_id, self.Post.title, func.substr(self.Post.text, 0, constant.PREVIEW_LENGTH), self.User.name, self.Post.owner, self.Post.date_created, self.Post.date_modified).join(self.User, self.User.username == self.Post.owner).filter(self.User.username == username).order_by(self.Post.post_id.desc()):
                previews.append(container.preview_factory(post_id, title, prev_text, name, username, date_created, date_modified))
        else:
            for post_id, title, prev_text, name, username, date_created, date_modified in self.session.query(self.Post.post_id, self.Post.title, func.substr(self.Post.text, 0, constant.PREVIEW_LENGTH), self.User.name, self.Post.owner, self.Post.date_created, self.Post.date_modified).join(self.User, self.User.username == self.Post.owner).order_by(self.Post.post_id.desc()):
                previews.append(container.preview_factory(post_id, title, prev_text, name, username, date_created, date_modified))
        return previews[::-1]