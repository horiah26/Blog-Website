"""
    Used to interact with the database section in config.ini
"""
import os
from flask import current_app, session
from .config import Config

class ConfigDB(Config):
    """Used to interact with the config.ini file"""
    def __init__(self):
        super().__init__()
        self.db_version = "1"


    def get_db_info(self):
        """Returns database configuration information"""
        try:
            json_data = super().load()
            db_config = {'database' : json_data ['database'],
                                'host' : json_data['host'],
                                'user' : json_data['user'],
                                'password' : json_data['password']
                            }
            return db_config
        except Exception:
            print("Couldn't load database configuration data. Check config.json file")

    def db_version_to_session(self):
        """Loads database version to current session"""
        json_data = super().load()
        if 'db_version' in json_data and json_data['db_version'] == self.db_version:
            session['db_version'] = json_data['db_version']
        else:
            session['db_version'] = None

    def update_db_version(self):
        """In the config.ini file updates db_version value to latest"""
        json_data = super().load()
        json_data['db_version'] = self.db_version
        session['db_version'] = self.db_version
        print(f"Database has been updated to version {self.db_version}")
        super().save(json_data)

    def config_file_exists(self):
        """Checks if database configuration file exists"""
        if current_app.config['DB_TYPE'] == 'db':
            return os.path.isfile(self.CONFIG_PATH)
        if current_app.config['DB_TYPE'] == 'memory':
            return True
        print("Error! DB_TYPE not configured correctly in app.config['DB_TYPE']. Type invalid")
        return False
