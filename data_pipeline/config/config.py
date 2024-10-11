import psycopg2

DB_NAME = 'nba_db'
DB_USER = 'nba_user'
DB_PASSWORD = 'nba_pass'
DB_HOST = 'localhost'
DB_PORT = '5432'

def get_db_connection():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cur = conn.cursor()
    return conn, cur