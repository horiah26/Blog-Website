"""Conects to the database"""
import psycopg2
from config.config_db import ConfigDB


class Connection():
    """Conects to the database"""
    def __init__(self):
        self.config = ConfigDB()

    def get(self):
        """Conects to the database"""
        db_config = self.config.get_db_info()
        try:
            return psycopg2.connect(database = db_config['database'],
                                user = db_config['user'],
                                password = db_config['password'],
                                host = db_config['host'])
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return None
