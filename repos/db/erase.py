from .connection import get_connection

def erase_all_posts():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("TRUNCATE TABLE posts RESTART IDENTITY;")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~All posts have been erased~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    conn.commit()
    cur.close()
    conn.close()