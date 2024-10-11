import psycopg2
import pandas as pd
DB_NAME = 'nba_db'
DB_USER = 'nba_user'
DB_PASSWORD = 'nba_pass'
DB_HOST = 'localhost'
DB_PORT = '5432'


def execute_sql_query(query):
    """
    Run the SQL query and return the results as a dataframe
    """
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    cur = conn.cursor()
    cur.execute(query)
    columns = [desc[0] for desc in cur.description]
    results = pd.DataFrame(cur.fetchall(), columns=columns)
    conn.close()
    return results