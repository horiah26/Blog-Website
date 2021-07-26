"""
    Used to interact with the config.ini file
"""
import json

class Config():
    """Used to interact with the config.ini file"""
    def __init__(self):
        self.CONFIG_PATH = 'config/config.json'

    def load(self):
        """Reads json_data from config file"""
        with open(self.CONFIG_PATH) as file:
            return json.loads(file.read())


    def save(self, new_data):
        """Writes json_data to config file"""
        with open(self.CONFIG_PATH, 'a') as file:

            json.dump(new_data.json, file)
