"""Database repo"""
import psycopg2
import datetime
from models.post import Post
from .create_tables import create_post_table
from .connection import get_connection

def create_table():
    """Creates tables"""
    conn = get_connection()
    create_post_table(conn)

def insert(post):
    """Add a new post"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO posts (title, text, owner, date_created, date_modified) \
        VALUES(%s, %s, %s, %s, %s)",
        (post.title, post.text, post.date_created, post.date_modified, post.owner))
    conn.commit()
    cur.close()
    conn.close()

def get(post_id):
    """Returns post by id"""
    conn = get_connection()
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

def delete(post_id):
    """Deletes post by id"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM posts WHERE post_id = %s;", (post_id,))
    rows_deleted = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()
    return rows_deleted

def update(post_id, title, text):
    """Updates post by id"""
    conn = get_connection()
    cur = conn.cursor()
    time_now = datetime.datetime.now().strftime("%H:%M %B %d %Y")
    cur.execute(
        "UPDATE posts SET title = %s, text = %s, date_modified = %s WHERE post_id = %s",
        (title, text, time_now, post_id))    
    conn.commit()
    cur.close()
    conn.close()

def get_all():
    """Returns all posts"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM posts;")
    posts = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return posts
