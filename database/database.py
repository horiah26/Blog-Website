"""Conects to the database"""
import psycopg2
from config.config_db import ConfigDB

class Database():
    """Handles database operations"""
    def __init__(self):
        self.config = ConfigDB()

    def get_connection(self):
        """Conects to the database"""
        db_config = self.config.get_db_info()
        try:
            return psycopg2.connect(database = db_config['database'],
                                user = db_config['user'],
                                password = db_config['password'],
                                host = db_config['host'])
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def create_update_tables(self):
        """Creates the posts table"""
        if self.config.config_file_exists() and not self.config.db_up_to_date():
            try:
                conn = self.get_connection()
                cur = conn.cursor()
                with open("database/schemas/schema.sql", "r") as command:
                    command_as_string = command.read()
                    cur.execute(command_as_string)
                cur.close()
                conn.commit()
                from database.hash_imported_passwords import HashImportedPasswords
                HashImportedPasswords().hash()
                self.config.update_db_version()
                print("Tables created or updated")
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
                print("Database version has not been updated")
