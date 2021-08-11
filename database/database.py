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

    def get_connection(self):
        """Conects to the database"""
        print(self.config_db.get_db_auth())#TODEL
        db_config = self.config_db.get_db_auth().json
        try:
            return psycopg2.connect(database = db_config['database'],
                                user = db_config['user'],
                                password = db_config['password'],
                                host = db_config['host'])
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def create_update_tables(self, password_hasher = Provide['password_hash']):
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
                password_hasher.hash()
                self.config_db.update_db_version()
                print("Tables created or updated")
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
                print("Database version has not been updated")
