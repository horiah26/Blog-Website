"""Conects to the database"""
import os
import json
import psycopg2

DB_PATH = 'database/db_config.json'

def get_connection():
    """Conects to the database"""
    try:
        with open(DB_PATH) as file:
            db_config = json.loads(file.read())

        return psycopg2.connect(database = db_config['database'],
                                user = db_config['user'],
                                password = db_config['password'],
                                host = db_config['host'])
    except Exception:
        print("Connection failed. Check db_config file")


def db_config_missing():
    """Checks if database configuration file exists"""
    return not os.path.isfile(DB_PATH)
