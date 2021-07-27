"""Puts all table names to current session"""

from flask import session

class TableNames():
    """Puts all table names to current session"""
    def __init__(self):
        pass

    def table_names(self):
        """Puts all table names to current session"""
        from .database import Database
        conn = Database().get_connection()
        cur = conn.cursor()
        session.pop('tables', None)
        cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
        as_tuple = cur.fetchall()
        table_list = []
        for table_as_tuple in as_tuple:
            table_list.append(table_as_tuple[0])
        cur.close()
        conn.commit()
        return table_list
