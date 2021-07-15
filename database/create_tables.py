"""Creates tables"""
import psycopg2

def create_post_table(conn):
    """Creates the posts table"""
    command = (
            """
            CREATE TABLE posts (
                    post_id  SERIAL PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    text TEXT NOT NULL,
                    owner VARCHAR(100) NOT NULL,
                    date_created VARCHAR(40) NOT NULL,
                    date_modified VARCHAR(40) NOT NULL
            )
            """)

    try:
        cur = conn.cursor()
        cur.execute(command)
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
