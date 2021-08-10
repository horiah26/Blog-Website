"""Database repo"""
import math
import datetime
import psycopg2
from static import constant

from containers.container import Container
from containers.db_container import DBContainer
from models.post import Post
from models.post_preview import PostPreview
from models.user import User

from .IPostRepo import IPostRepo

container = Container()
db = DBContainer().database_factory()

class RepoPostsDB(IPostRepo):
    """Repository for posts that communicates with the database"""
    def __init__(self, seed = None):
        """Initializes class and adds posts from seed if present"""
        if seed is not None and self.get_all() is not None and len(self.get_all()) == 0:
            for post in seed:
                self.insert(post)

    def insert(self, post):
        """Add a new post"""
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO posts (title, text, owner, date_created, date_modified) \
            VALUES(%s, %s, %s, %s, %s)",
            (post.title, post.text, post.owner, post.date_created, post.date_modified))

        conn.commit()
        cur.close()
        conn.close()

    def get(self, post_id):
        """Returns post by id"""
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT post_id, title, text, owner, posts.date_created, posts.date_modified, name FROM posts JOIN users ON owner = username WHERE post_id = %s;", (post_id,))
        post = cur.fetchone()

        conn.commit()
        cur.close()
        conn.close()

        if post is None:
            print("ERROR: Post not found, incorrect id")
        else:
            return (Post(post[0], post[1], post[2], post[3], post[4], post[5]), post[6])

    def delete(self, post_id):
        """Deletes post by id"""
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM posts WHERE post_id = %s;", (post_id,))
        conn.commit()
        cur.close()
        conn.close()

    def update(self, post_id, title, text):
        """Updates post by id"""
        conn = db.get_connection()
        cur = conn.cursor()
        time_now = datetime.datetime.now().strftime("%B %d %Y - %H:%M")
        cur.execute(
            "UPDATE posts SET title = %s, text = %s, date_modified = %s WHERE post_id = %s",
            (title, text, time_now, post_id))
        conn.commit()
        cur.close()
        conn.close()

    def get_all(self):
        """Returns all posts"""
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM posts;")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        posts = []
        for row in rows:
            posts.append(Post(row[0], row[1], row[2], row[3], row[4], row[5]))
        return posts

    def get_previews(self, username = None, per_page = 6, page_num = 1):
        """Returns previews of posts posts"""
        conn = db.get_connection()
        cur = conn.cursor()
        offset_nr = (page_num - 1) * per_page

        if username:
            cur.execute("SELECT post_id, title, LEFT(text, %s), name, users.username, posts.date_created, posts.date_modified FROM posts JOIN users ON owner = username WHERE username = %s ORDER BY post_id DESC OFFSET %s LIMIT %s;", [constant.PREVIEW_LENGTH, username, offset_nr, per_page])
        else:
            cur.execute("SELECT post_id, title, LEFT(text, %s), name, users.username, posts.date_created, posts.date_modified FROM posts JOIN users ON owner = username ORDER BY post_id DESC OFFSET %s LIMIT %s;", [constant.PREVIEW_LENGTH, offset_nr, per_page])
        previews = cur.fetchall()
        
        if username:
            cur.execute ("SELECT COUNT(*) FROM posts WHERE owner = %s", [username])
        else:
            cur.execute ("SELECT COUNT(*) FROM posts")

        total_posts = cur.fetchone()[0]
        total_pages = math.ceil(total_posts / per_page)

        cur.close()
        conn.close()
        posts = []

        for row in previews:
            posts.append(PostPreview(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
        return (posts, total_pages)

    def next_id(self):
        """Created to be compatible with post_repo_memory.
            Id is assigned automatically by database"""
        return 0
