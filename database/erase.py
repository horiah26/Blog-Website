from database.connection import Connection
connection = Connection()

def erase_all_posts():
    conn = connection.get()
    cur = conn.cursor()
    cur.execute("TRUNCATE TABLE posts RESTART IDENTITY;")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~All posts have been erased~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    conn.commit()
    cur.close()
    conn.close()