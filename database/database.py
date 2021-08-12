"""Conects to the database"""
import psycopg2
from dependency_injector.wiring import inject, Provide

class Database():
    """Handles database operations"""
    @inject
    def __init__(self,
                config = Provide['config'],
                config_db = Provide['config_db']):
        self.config = config
        self.config_db = config_db

    def create_update_tables(self):
        """Creates the posts table"""
        if self.config.config_file_exists() and not self.config_db.db_up_to_date():                     
            try:
                conn = self.get_connection()
                cur = conn.cursor()

                with open("database/schemas/schema.sql", "r") as command:
                    command_as_string = command.read()
                    cur.execute(command_as_string)

                cur.close()
                conn.commit()
                self.hash_passwords()
                self.config_db.update_db_version()
                print("Tables created or updated")
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
                print("Database version has not been updated")
    @inject
    def hash_passwords(self, hasher = Provide['hasher'], user_repo = Provide['user_repo']):
        user_repo = user_repo
        for user in user_repo.get_all():
            if user.password == user.username:
                user_repo.update(user.username, user.name, user.email, hasher.hash(user.password))

    def get_connection(self):
        """Conects to the database"""
        db_config = self.config_db.get_db_auth().json
        try:
            return psycopg2.connect(database = db_config['database'],
                                user = db_config['user'],
                                password = db_config['password'],
                                host = db_config['host'])
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)