from database.connection import Connection
connection = Connection()

def erase_all():
    conn = connection.get()
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS posts;")
    cur.execute("DROP TABLE IF EXISTS posts_1;")
    cur.execute("DROP TABLE IF EXISTS users;")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~All posts have been erased~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    conn.commit()
    cur.close()
    conn.close()