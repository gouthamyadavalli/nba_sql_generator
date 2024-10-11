from nba_api.stats.static import teams, players
from nba_api.stats.endpoints import leaguegamefinder
from nba_api.stats.endpoints import playergamelog
import pandas as pd

def fetch_teams():
    # Fetches team data from the NBA API and stores it in a database and return a dataframe
    
    # Fetch team data from the NBA API
    teams_data = teams.get_teams()

    # Convert the data to a dataframe
    teams_df = pd.DataFrame(teams_data)

    return teams_df

def fetch_players():
    # Fetches player data from the NBA API and stores it in a database and return a dataframe
    
    # Fetch player data from the NBA API
    players_data = players.get_players()

    # Convert the data to a dataframe
    players_df = pd.DataFrame(players_data)

    return players_df

def fetch_games():
    # Fetch games for the last 10 seasons from the NBA API
    # and stores it in a database and return a dataframe

    # Fetch game data from the NBA API
    all_games = {}

    for season in range(2010, 2020):
        season_str = f"{season}-{str(season + 1)[2:]}"
        game_finder = leaguegamefinder.LeagueGameFinder(season_nullable=season_str)

        games = game_finder.get_data_frames()[0]
        games = games[['GAME_ID', 'GAME_DATE', 'TEAM_ID', 'MATCHUP', 'PTS']].to_dict(orient='records')

        for game in games:
            game_id = game["GAME_ID"]
            if game_id in all_games:
                all_games[game_id]["TEAM_ID_2"] = game["TEAM_ID"]
                all_games[game_id]["TEAM_2"] = game["MATCHUP"][:3]
                all_games[game_id]["PTS_2"] = game["PTS"]
            else:
                all_games[game_id] = {
                    "GAME_DATE": game["GAME_DATE"],
                    "TEAM_ID_1": game["TEAM_ID"],
                    "TEAM_1": game["MATCHUP"][:3],
                    "PTS_1": game["PTS"]
                }

    # Discrad all the games where either of the team does not have a valid team id, check it from the result of fetch_teams()
    teams_df = fetch_teams()

    all_games = {game_id: game for game_id, game in all_games.items() if game["TEAM_ID_1"] in teams_df["id"].values and game["TEAM_ID_2"] in teams_df["id"].values}

    return pd.DataFrame(all_games).T

def fetch_stats(players_df):
    # Fetches player stats from the NBA API and stores it in a database and return a dataframe

    # Fetch player stats from the NBA API
    player_stats = []

    for player_id in players_df["id"]:
        # Continue if player is not active
        if players_df[players_df["id"] == player_id]["is_active"].values[0]:
            for season in range(2010, 2020):
                season_str = f"{season}-{str(season + 1)[2:]}"
                player_gamelog = playergamelog.PlayerGameLog(player_id=player_id, season=season_str)

                player_stats.extend(player_gamelog.get_data_frames())
    return pd.concat(player_stats)

