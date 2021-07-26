"""Creates tables"""
import datetime
import psycopg2
from werkzeug.security import generate_password_hash

class CreateTables():
    """Creates the tables"""
    def create_tables(self, conn):
        """Creates the posts table"""
        try:
            cur = conn.cursor()
            with open("database/schemas/schema.sql", "r") as command:
                command_as_string = command.read()
                cur.execute(command_as_string)
            cur.close()
            conn.commit()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        cur = conn.cursor()
        cur.execute("SELECT	DISTINCT owner FROM posts WHERE owner NOT IN(SELECT username FROM users);")
        owners = cur.fetchall()
        owners = list(dict.fromkeys(owners))
        time_now = datetime.datetime.now().strftime("%B %d %Y - %H:%M")
        for owner in owners:
            owner = owner[0]
            cur.execute(
                "INSERT INTO users (username, name, email, password, date_created, date_modified) \
                VALUES(%s, %s, %s, %s, %s, %s)",
                (owner, owner, owner, generate_password_hash(owner), time_now, time_now))
        cur.close()
        conn.commit()

        cur = conn.cursor()
        cur.execute("ALTER TABLE posts ADD FOREIGN KEY (owner) REFERENCES users(username)")
        cur.close()
        conn.commit()
