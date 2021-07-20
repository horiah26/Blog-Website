"""Checks if database configuration file exists"""
import os
from config.config import Config
config = Config()

class ConfigExists():
    """Checks if database configuration file exists"""
    def check(self, app):
        """Checks if database configuration file exists"""        
        self.DB_PATH = config.CONFIG_PATH

        if app.config['DB_TYPE'] == 'db':
            return os.path.isfile(self.DB_PATH)

        if app.config['DB_TYPE'] == 'memory':
            return True

        print("Error! DB_TYPE not configured correctly in app.config['DB_TYPE']. Type invalid")
        return False