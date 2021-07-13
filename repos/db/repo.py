import psycopg2
from .create_table import create_post_table
from .connection import get_connection
from models.post import Post

def create_table():    
    conn = get_connection()
    create_table.create_post_table(conn)

def insert(post):        
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO posts (title, text, owner, date_created, date_modified) VALUES(%s, %s, %s, %s, %s)", 
                (post.title, post.text, post.date_created, post.date_modified, post.owner))
    conn.commit()
    cur.execute("SELECT * FROM posts;")
    
    print(cur.fetchall())
    cur.close()
    conn.close()

def get(id):    
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM posts WHERE id = %s;", (id,))

    post = cur.fetchone()  
    conn.commit()
    cur.close()
    conn.close()
    if post is not None:
        return Post(post[0], post[1], post[2], post[3], post[4], post[5])
    else:
        print("ERROR: Post not found, incorrect id")

def delete(id):    
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM posts WHERE id = %s;", (id,))    
    rows_deleted = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()
    return rows_deleted