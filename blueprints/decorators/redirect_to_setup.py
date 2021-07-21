"""Redirects to setup page if db not configured"""
from functools import wraps
from flask import redirect, url_for
from database.connection import Connection
from database.create_tables import CreateTables

connection = Connection()
create_tables = CreateTables()

def redirect_to_setup(app):
    """Redirects to setup page if db not configured"""
    def helper_function(f):
        """Added so app could be inserted as a parameter in the other wrapper"""
        @wraps(f)
        def redirect_if_no_db(*args, **kwargs):
            """Redirects to setup page if db not configured"""
            if not connection.config_exists(app):
                return redirect(url_for('setup.setup_db'))
            create_tables.create_tables(connection.get())
            return f(*args, **kwargs)
        return redirect_if_no_db
    return helper_function
