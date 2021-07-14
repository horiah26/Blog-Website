"""Conects to the database"""
import psycopg2

def get_connection():
    """Conects to the database"""
    return psycopg2.connect(database="postgres",
                            user="postgres",
                            password="123456",
                            host="localhost")
