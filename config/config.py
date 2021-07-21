"""
    Used to interact with the config.ini file
"""
import json

class Config():
    """Used to interact with the config.ini file"""
    def __init__(self):
        self.CONFIG_PATH = 'config/config.json'

    def get_db_info(self):
        """Returns database configuration information"""
        try:
            with open(self.CONFIG_PATH) as file:
                config = json.loads(file.read())
                db_config = {'database' : config['database'],
                                 'host' : config['host'],
                                 'user' : config['user'],
                                 'password' : config['password']
                                }
                return db_config
        except Exception:
            print("Couldn't load database configuration data. Check config.json file")

    def append(self, db_auth):
        """Appends instructions to config file"""
        with open(self.CONFIG_PATH, 'a') as file:
            json.dump(db_auth.json, file)
