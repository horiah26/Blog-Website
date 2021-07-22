"""Conects to the database"""
import os
import psycopg2
from flask import current_app
from config.config import Config

#config = Config() TODEL

class Connection():
    """Conects to the database"""
    def __init__(self):
        self.config = Config()

    def get(self):
        """Conects to the database"""
        db_config = self.config.get_db_info()

        return psycopg2.connect(database = db_config['database'],
                                user = db_config['user'],
                                password = db_config['password'],
                                host = db_config['host'])

    #def config_exists(self):
    #    """Checks if database configuration file exists"""
    #    if current_app.config['DB_TYPE'] == 'db':
    #        return os.path.isfile(self.config.CONFIG_PATH)
    #    if current_app.config['DB_TYPE'] == 'memory':
    #        return True
    #    print("Error! DB_TYPE not configured correctly in app.config['DB_TYPE']. Type invalid")
    #    return False
