"""Conects to the database"""
import os
import psycopg2
from config.config import Config

config = Config()

class Connection():
    """Conects to the database"""
    def __init__(self):
        self.config_manager = Config()

    def get(self):
        """Conects to the database"""
        db_config = config.get_db_info()

        return psycopg2.connect(database = db_config['database'],
                                user = db_config['user'],
                                password = db_config['password'],
                                host = db_config['host'])

    def config_exists(self, app):
        """Checks if database configuration file exists"""
        if app.config['DB_TYPE'] == 'db':
            return os.path.isfile(config.CONFIG_PATH)
        if app.config['DB_TYPE'] == 'memory':
            return True
        print("Error! DB_TYPE not configured correctly in app.config['DB_TYPE']. Type invalid")
        return False
