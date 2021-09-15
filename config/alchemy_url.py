"""Creates the url for engine configuration in alchemy repos"""


class AlchURL:
    """Creates the url for engine configuration in alchemy repos"""
    def __init__(self, config_db):
        self.db_auth = config_db.get_db_auth().json
        self.port = '5432'

    def get_url(self):
        """Creates the url for engine configuration in alchemy repos"""
        url = 'postgresql://' + self.db_auth['user'] + ':' + self.db_auth['password'] + '@' + self.db_auth['host'] \
              + ':' + self.port + '/' + self.db_auth['database']
        return url
