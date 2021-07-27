"""Memory posts repo"""
import datetime
import psycopg2

from flask import flash
from models.user import User
from database.database import Database
from .IUserRepo import IUserRepo

db = Database()

class RepoUserDB(IUserRepo):
    """Repo for posts in memory"""
    def __init__(self, seed = None):
        if seed is not None and len(self.get_all()) == 0:
            for user in seed:
                self.insert(user)

    def insert(self, user):
        """Add a new user"""
        conn = db.get_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO users (username, name, email, password, date_created, date_modified) \
                VALUES(%s, %s, %s, %s, %s, %s)",
                (user.username, user.name, user.email, user.password, user.date_created, user.date_modified))

        except Exception as error:
            print(error)
            flash(error)

        conn.commit()
        cur.close()
        conn.close()

    def get(self, username):
        """Returns user object by username"""
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s;", (username,))
        user = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()

        if user is None:
            print("ERROR: Post not found, incorrect username")
        else:
            return User(user[0], user[1], user[2], user[3], user[4], user[5])

    def delete(self, username):
        """Deletes user by username"""
        conn = db.get_connection()
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM users WHERE username = %s;", (username,))
        except Exception as error:
            print(error)
            flash(error)
        conn.commit()
        cur.close()
        conn.close()

    def update(self, username, name, email, password):
        """Updates user by id"""
        conn = db.get_connection()
        cur = conn.cursor()
        time_now = datetime.datetime.now().strftime("%B %d %Y - %H:%M")
        cur.execute(
            "UPDATE users SET name = %s, email = %s, password = %s, date_modified = %s WHERE username = %s",
            (name, email, password, time_now, username))
        conn.commit()
        cur.close()
        conn.close()

    def get_all(self):
        """Returns all users"""
        conn = db.get_connection()
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM users;")
        except Exception as error:
            print(error)
            flash(error)
            return []
        rows = cur.fetchall()
        cur.close()
        conn.close()
        users = []
        for row in rows:
            users.append(User(row[0], row[1], row[2], row[3], row[4], row[5]))
        return users
