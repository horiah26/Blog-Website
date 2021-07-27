"""Creates or updates table if database version is old"""
from functools import wraps
from flask import session
from database.database import Database
from config.config_db import ConfigDB

def create_tables(f):
    """decorator"""
    @wraps(f)
    def wrapped(*args, **kwargs):
        """decorator"""
        if 'db_version' not in session:
            ConfigDB().db_version_to_session()
        Database().create_update_tables()
        return f(*args, **kwargs)
    return wrapped
