import psycopg2
import psycopg2.extras

conn = psycopg2.connect(database="postgres", user="postgres", password="starwars19", host="localhost")

#cursor = conn.cursor()
#cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

#cursor.execute("CREATE TABLE first_table (id SERIAL PRIMARY KEY, name VARCHAR);")

#cursor.execute("INSERT INTO first_table (name) VALUES(%s)", ("Cristina",))

#cursor.execute("SELECT * FROM first_table;")
#print(cursor.fetchall())

#cursor.execute("SELECT * FROM first_table WHERE id = %s;", (1,))
#print(cursor.fetchone()['name'])

with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
    cur.execute("SELECT * FROM first_table WHERE id=%s;", (1,))

    print(cur.fetchone()['name'])

conn.commit()
cur.close()
#conn.close()