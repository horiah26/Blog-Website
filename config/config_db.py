"""
    Used to interact with the config.ini file
"""
import os
from flask import current_app
from .config import Config

class ConfigDB(Config):
    """Used to interact with the config.ini file"""

    def get_db_info(self):
        """Returns database configuration information"""
        try:
            json_data = self.load()
            db_config = {'database' : json_data ['database'],
                                'host' : json_data['host'],
                                'user' : json_data['user'],
                                'password' : json_data['password']
                            }
            return db_config
        except Exception:
            print("Couldn't load database configuration data. Check config.json file")

    def config_file_exists(self):
        """Checks if database configuration file exists"""
        if current_app.config['DB_TYPE'] == 'db':
            return os.path.isfile(self.CONFIG_PATH)
        if current_app.config['DB_TYPE'] == 'memory':
            return True
        print("Error! DB_TYPE not configured correctly in app.config['DB_TYPE']. Type invalid")
        return False
