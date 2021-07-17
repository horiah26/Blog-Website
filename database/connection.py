"""Conects to the database"""
import os
import json
import psycopg2

class Connection():
    """Conects to the database"""
    def __init__(self):
        self.DB_PATH = 'database/db_config.json'

    def get(self):
        """Conects to the database"""
        try:
            with open(self.DB_PATH) as file:
                db_config = json.loads(file.read())

            return psycopg2.connect(database = db_config['database'],
                                    user = db_config['user'],
                                    password = db_config['password'],
                                    host = db_config['host'])
        except Exception:
            print("Connection failed. Check db_config file")


    def db_config_missing(self):
        """Checks if database configuration file exists"""
        return not os.path.isfile(self.DB_PATH)
