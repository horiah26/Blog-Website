"""Database repo"""
import datetime
import psycopg2
from models.post import Post
from models.post_preview import PostPreview
from database.connection import Connection
from .IPost import IPost

connection = Connection()

class RepoPostsDB(IPost):
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
        #try:
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
        cur.execute("SELECT LEFT(text, 180) FROM posts;")
        text_preview = cur.fetchall()         

        cur.execute("SELECT * INTO temp_table FROM posts;")
        cur.execute("ALTER TABLE temp_table DROP COLUMN text;")
        cur.execute("SELECT * FROM temp_table;")
        columns_except_text = cur.fetchall()   
        cur.execute("DROP TABLE temp_table;")
        cur.close()
        conn.close()
        rows=[columns_except_text, text_preview]

        posts = []
        for index in range(len(text_preview)):
            current_column = columns_except_text[index]
            posts.append(PostPreview(current_column[0],
                                    current_column[1],
                                    text_preview[index],
                                    current_column[2],
                                    current_column[3],
                                    current_column[4]))
            posts.sort(key=lambda x: x.post_id)
        return posts

    def next_id(self):
        """Created to be compatible with post_repo_memory.
            Id is assigned automatically by database"""
        return 0
