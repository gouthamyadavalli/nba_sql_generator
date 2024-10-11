import sys
sys.path.append('/opt/airflow/dags/src/data_pipeline/config')
from config.config import get_db_connection

def insert_teams(teams_df):
    conn, cur = get_db_connection()

    for index, row in teams_df.iterrows():
        cur.execute(
            "INSERT INTO teams (team_id, team_name, abbreviation, city) VALUES (%s, %s, %s, %s)",
            (row["id"], row["full_name"], row["abbreviation"], row["city"])
        )

    conn.commit()
    cur.close()
    conn.close()

def insert_players(players_df):
    conn, cur = get_db_connection()

    for index, row in players_df.iterrows():
        cur.execute(
            "INSERT INTO players (player_id, player_name, is_active) VALUES (%s, %s, %s)",
            (row["id"], row["full_name"], row["is_active"])
        )

    conn.commit()
    cur.close()
    conn.close()

def insert_games(games_df):
    conn, cur = get_db_connection()

    for index, row in games_df.iterrows():
        cur.execute(
            "INSERT INTO games (game_id, game_date, team_id_1, team_1, pts_1, team_id_2, team_2, pts_2) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (row.name, row["GAME_DATE"], row["TEAM_ID_1"], row["TEAM_1"], row["PTS_1"], row["TEAM_ID_2"], row["TEAM_2"], row["PTS_2"])
        )

    conn.commit()
    cur.close()
    conn.close()

def insert_player_stats(player_stats_df):
    conn, cur = get_db_connection()

    for index, row in player_stats_df.iterrows():
        cur.execute(
            "INSERT INTO player_stats (game_id, player_id, points, rebounds, assists, steals, blocks, turnovers, field_goal_percentage) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (row["GAME_ID"], row["PLAYER_ID"], row["PTS"], row["REB"], row["AST"], row["STL"], row["BLK"], row["TO"], row["FG_PCT"])
        )

    conn.commit()
    cur.close()
    conn.close()

