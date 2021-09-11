"""
    Used to interact with the config.ini file
"""
import os
import json
from flask import current_app


class Config:
    """Used to interact with the config.ini file"""
    def __init__(self):
        self.CONFIG_PATH = 'config/config.json'

    def load(self):
        """Reads json_data from config file"""
        with open(self.CONFIG_PATH) as file:
            return json.loads(file.read())

    def save(self, new_data):
        """Writes json_data to config file"""
        try:
            os.remove(self.CONFIG_PATH)
        except:
            pass
        with open(self.CONFIG_PATH, 'w') as file:
            json.dump(new_data, file)

    def config_file_exists(self):
        """Checks if database configuration file exists"""
        if current_app.config['DB_TYPE'] in ['db', 'alchemy']:
            return os.path.isfile(self.CONFIG_PATH)
        if current_app.config['DB_TYPE'] == 'memory':
            return True
        print("Error! DB_TYPE not configured correctly in app.config['DB_TYPE']. Type invalid")
        return False
