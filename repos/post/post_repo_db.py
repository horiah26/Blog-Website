"""Database repo"""
import datetime
import psycopg2
from models.post import Post
from models.post_preview import PostPreview
from database.connection import Connection
from static import constant
from .IPostRepo import IPostRepo

connection = Connection()

class RepoPostsDB(IPostRepo):
    """Repository for posts that communicates with the database"""
    def __init__(self, seed = None):
        """Initializes class and adds posts from seed if present"""
        if seed is not None and self.get_all() is not None and len(self.get_all()) == 0:
            for post in seed:
                self.insert(post)

    def insert(self, post):
        """Add a new post"""
        conn = connection.get()
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
        conn = connection.get()
        cur = conn.cursor()
        cur.execute("SELECT * FROM posts WHERE post_id = %s;", (post_id,))
        post = cur.fetchone()

        conn.commit()
        cur.close()
        conn.close()

        if post is None:
            print("ERROR: Post not found, incorrect id")
        else:
            return Post(post[0], post[1], post[2], post[3], post[4], post[5])

    def delete(self, post_id):
        """Deletes post by id"""
        conn = connection.get()
        cur = conn.cursor()
        cur.execute("DELETE FROM posts WHERE post_id = %s;", (post_id,))
        conn.commit()
        cur.close()
        conn.close()

    def update(self, post_id, title, text):
        """Updates post by id"""
        conn = connection.get()
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
        conn = connection.get()
        cur = conn.cursor()
        cur.execute("SELECT * FROM posts;")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        posts = []
        for row in rows:
            posts.append(Post(row[0], row[1], row[2], row[3], row[4], row[5]))
        return posts

    def get_previews(self):
        """Returns previews of posts posts"""
        conn = connection.get()
        cur = conn.cursor()
        cur.execute("SELECT post_id, title, LEFT(text, %s), name, users.date_created, users.date_modified FROM posts JOIN users ON owner = username;", [constant.PREVIEW_LENGTH])
        previews = cur.fetchall()
        first = cur.fetchone()
        print(first)
        cur.close()
        conn.close()

        posts = []
        for row in previews:
            posts.append(PostPreview(row[0], row[1], row[2], row[3], row[4], row[5]))
        return posts

    def next_id(self):
        """Created to be compatible with post_repo_memory.
            Id is assigned automatically by database"""
        return 0
