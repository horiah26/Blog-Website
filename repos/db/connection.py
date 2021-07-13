import psycopg2

def get_connection():
    return psycopg2.connect(database="postgres", user="postgres", password="123456", host="localhost")