import psycopg2
from config import DATABASE_CONFIG

def get_db_connection():
    return psycopg2.connect(
        dbname=DATABASE_CONFIG['dbname'],
        user=DATABASE_CONFIG['user'],
        password=DATABASE_CONFIG['password'],
        host=DATABASE_CONFIG['host'],
        port=DATABASE_CONFIG['port']
    )