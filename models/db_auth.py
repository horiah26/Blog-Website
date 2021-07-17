"""Clas that encapsulates database configuration data"""
class DbAuth():
    """Clas that encapsulates database configuration data"""
    def __init__(self, database, host, user, password):
        self.database = database
        self.host = host
        self.user = user
        self.password = password
        self.json = {
                    "database" : database,
                    "host": host,
                    "user" : user,
                    "password" : password
                    }
