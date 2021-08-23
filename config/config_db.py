"""
    Used to interact with the database section in config.ini
"""
from models.db_auth import DbAuth
from .config import Config

class ConfigDB(Config):
    """Used to interact with the config.ini file"""
    def __init__(self):
        super().__init__()
        self.db_version = "4"

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
            return True
        return False

    def update_db_version(self):
        """In the config.ini file updates db_version value to latest"""
        json_data = super().load()
        json_data['db_version'] = self.db_version
        print(f"Database has been updated to version {self.db_version}")
        super().save(json_data)

    def save(self, db_auth):
        """Saves data kept in DbAuth class to config.ini"""
        new_data = db_auth.json
        json_data = {}

        try:
            json_data = super().load()
        except:
            pass

        json_data['host'] = new_data['host']
        json_data['user'] = new_data['user']
        json_data['password'] = new_data['password']
        json_data['database'] = new_data['database']

        super().save(json_data)
