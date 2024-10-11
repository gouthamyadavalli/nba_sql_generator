import psycopg2

# Database connection parameters
DB_NAME = 'nba_db'
DB_USER = 'nba_user'
DB_PASSWORD = 'nba_pass'
DB_HOST = 'localhost'
DB_PORT = '5432'

def create_tables():
    commands = (
        """ 
        CREATE TABLE IF NOT EXISTS teams (
            id SERIAL PRIMARY KEY,
            team_id INTEGER,
            team_name VARCHAR(50),
            abbreviation VARCHAR(3),
            city VARCHAR(50),
            
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS players (
            id SERIAL PRIMARY KEY,
            player_id INTEGER,
            player_name VARCHAR(50),
            is_active BOOLEAN
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS games (
            id SERIAL PRIMARY KEY,
            game_id INTEGER,
            game_date DATE,
            team_id_1 INTEGER,
            team_1 VARCHAR(3),
            pts_1 INTEGER,
            team_id_2 INTEGER,
            team_2 VARCHAR(3),
            pts_2 INTEGER
        )
        """,
        """
        CREATE TABLE PlayerStats (
            stat_id SERIAL PRIMARY KEY,
            game_id VARCHAR(20) REFERENCES Games(game_id),
            player_id INTEGER REFERENCES Players(player_id),
            points INTEGER,
            rebounds INTEGER,
            assists INTEGER,
            steals INTEGER,
            blocks INTEGER,
            turnovers INTEGER,
            field_goal_percentage DECIMAL(5, 2)
        )
        """
    )

    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
        cur = conn.cursor()

        # Execute each SQL command to create the tables
        for command in commands:
            cur.execute(command)

        # Commit the changes and close the connection
        conn.commit()
        cur.close()
        print("Tables created successfully.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
    finally:
        if conn is not None:
            conn.close()
    return