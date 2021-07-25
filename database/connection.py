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
