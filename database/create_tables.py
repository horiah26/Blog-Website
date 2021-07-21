"""Creates tables"""
import psycopg2

class CreateTables():
    """Creates the tables"""
    def create_tables(self, conn):
        """Creates the posts table"""
        try:
            cur = conn.cursor()
            with open("database/schemas/schema.sql", "r") as command:
                cur.execute(command)
            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
