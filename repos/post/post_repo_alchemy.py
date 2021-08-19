"""SQLAlchemy repo"""

import math
from datetime import datetime
from static import constant

from sqlalchemy.sql import func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.post import Post
from models.date import Date
from models.post_preview import PostPreview

from .IPostRepo import IPostRepo

class RepoPostsAlchemy(IPostRepo):
    """SQLAlchemy repo"""
    def __init__(self, config, alch_url, seed = None):
        """Initializes class and adds posts from seed if present"""
        db = create_engine(alch_url.get_url())

        Session = sessionmaker(db)
        self.session = Session()

        Base = automap_base()
        Base.prepare(db, reflect=True)

        self.Post = Base.classes.posts
        self.User = Base.classes.users

        if seed is not None and config.config_file_exists() and self.get_all() is not None and len(self.get_all()) == 0:
            for post in seed:
                self.insert(post)

    def insert(self, post):
        """Add a new post"""
        new_post = self.Post(post_id = post.post_id, title = post.title, text = post.text, owner = post.owner, img_id = post.img_id, date_created = post.date.created, date_modified = post.date.modified)
        self.session.add(new_post)
        self.session.commit()

    def get(self, post_id):
        """Returns post by id"""
        post = self.session.query(self.Post.post_id, self.Post.title, self.Post.text, self.Post.owner, self.Post.img_id, self.Post.date_created, self.Post.date_modified, self.User.name).join(self.User, self.User.username == self.Post.owner).filter(self.Post.post_id == post_id).first()
        return (Post(post[0], post[1], post[2], post[3], post[4], Date(post[5], post[6])), post[7])

    def get_all(self):
        """Returns all posts"""
        query_posts = self.session.query(self.Post).all()
        posts = []
        for post in query_posts:
            posts.append(Post(post.post_id, post.title, post.text, post.owner, post.img_id, Date(post.date_created, post.date_modified)))
        return posts

    def update(self, post_id, title, text, img_id):
        """Updates post by id"""
        post = self.session.query(self.Post).filter(self.Post.post_id == post_id).first()
        post.title = title
        post.text = text
        post.img_id = img_id
        post.date_modified = datetime.now().strftime("%B %d %Y - %H:%M")
        self.session.commit()

    def delete(self, post_id):
        """Deletes post by id"""
        post = self.session.query(self.Post).filter(self.Post.post_id == post_id).first()
        self.session.delete(post)
        self.session.commit()

    def get_previews(self, username = None, per_page = 6, page_num = 1):
        """Returns previews of posts posts"""
        offset_nr = (page_num - 1) * per_page
        previews = []

        if username:
            total_posts = self.session.query(self.Post).filter(self.Post.owner == username).count()
        else:
            total_posts = self.session.query(self.Post).count()

        total_pages = math.ceil(total_posts / per_page)

        if username:
            for post_id, title, prev_text, name, username, img_id, date_created, date_modified in self.session.query(self.Post.post_id, self.Post.title, func.substr(self.Post.text, 0, constant.PREVIEW_LENGTH), self.User.name, self.Post.owner, self.Post.img_id, self.Post.date_created, self.Post.date_modified).join(self.User, self.User.username == self.Post.owner).filter(self.User.username == username).order_by(self.Post.post_id.desc()).slice(offset_nr, offset_nr + per_page):
                previews.append(PostPreview(post_id, title, prev_text, name, username, img_id, Date(date_created, date_modified)))
        else:
            for post_id, title, prev_text, name, username, img_id, date_created, date_modified in self.session.query(self.Post.post_id, self.Post.title, func.substr(self.Post.text, 0, constant.PREVIEW_LENGTH), self.User.name, self.Post.owner, self.Post.img_id, self.Post.date_created, self.Post.date_modified).join(self.User, self.User.username == self.Post.owner).order_by(self.Post.post_id.desc()).limit(per_page).offset(offset_nr):
                previews.append(PostPreview(post_id, title, prev_text, name, username, img_id, Date(date_created, date_modified)))

        return (previews, total_pages)

    def next_id(self):
        """Returns next id"""
        return self.session.query(func.max(self.Post.post_id)).first()[0] + 1
