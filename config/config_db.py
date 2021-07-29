"""
    Used to interact with the database section in config.ini
"""
import os
from flask import session, current_app
from .config import Config
from models.db_auth import DbAuth

class ConfigDB(Config):
    """Used to interact with the config.ini file"""
    def __init__(self):
        super().__init__()
        self.db_version = "1"

    def get_db_auth(self):
        """Returns database configuration information"""
        try:
            json_data = super().load()
            return DbAuth(json_data['database'], json_data['host'], json_data['user'], json_data['password'])
        except Exception:
            print("Couldn't load database configuration data. Check config.json file")

    def db_up_to_date(self):
        """Loads database version to current session"""
        json_data = super().load()
        if 'db_version' in json_data and json_data['db_version'] == self.db_version:
            print ("Database up to date")
            return True
        return False

    def update_db_version(self):
        """In the config.ini file updates db_version value to latest"""
        json_data = super().load()
        json_data['db_version'] = self.db_version
        session['db_version'] = self.db_version
        print(f"Database has been updated to version {self.db_version}")
        super().save(json_data)
