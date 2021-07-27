"""Creates or updates table if database version is old"""
from functools import wraps
from flask import session
from database.database import Database
from config.config_db import ConfigDB
db = Database()
cfg = ConfigDB()

def create_tables(f):
    """decorator"""
    @wraps(f)
    def wrapped(*args, **kwargs):
        """decorator"""
        if 'db_version' not in session:
            cfg.db_version_to_session()
        if session['db_version'] != cfg.db_version:
            if db.get_connection():
                db.create_update_tables()

        return f(*args, **kwargs)
    return wrapped
