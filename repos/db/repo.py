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
    """Defines the post attributes"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO posts (title, text, owner, date_created, date_modified) \
        VALUES(%s, %s, %s, %s, %s)",
        (post.title, post.text, post.date_created, post.date_modified, post.owner))
    conn.commit()
    cur.execute("SELECT * FROM posts;")
    cur.close()
    conn.close()

def get(id):
    """Returns post by id"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM posts WHERE id = %s;", (id,))
    post = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()

    if post is None:
        print("ERROR: Post not found, incorrect id")
    else:
        return Post(post[0], post[1], post[2], post[3], post[4], post[5])

def delete(id):
    """Deletes post by id"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM posts WHERE id = %s;", (id,))
    rows_deleted = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()
    return rows_deleted

def update(id, title, text):
    """Updates post by id"""
    conn = get_connection()
    cur = conn.cursor()
    time_now = datetime.datetime.now().strftime("%H:%M  %d.%B.%Y")
    cur.execute(
        "UPDATE posts SET title = %s, text = %s, date_modified = %s WHERE id = %s",
        (title, text, time_now, id))    
    conn.commit()
    cur.close()
    conn.close()