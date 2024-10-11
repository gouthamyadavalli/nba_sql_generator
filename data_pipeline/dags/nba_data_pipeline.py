from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import sys
sys.path.append('/opt/airflow/dags/src/data_pipeline/scripts')
sys.path.append('/opt/airflow/dags/src/data_pipeline/config')
from scripts.create_tables import create_tables
from scripts.fetch_data import fetch_teams, fetch_players, fetch_games, fetch_stats
from scripts.insert_data import insert_teams, insert_players, insert_games, insert_player_stats

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 10, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'nba_data_pipeline',
    default_args=default_args,
    description='An Airflow DAG for fetching NBA data using nba_api and loading it into a database',
    schedule_interval=timedelta(days=1),
)

create_tables_task = PythonOperator(
    task_id='create_tables',
    python_callable=create_tables,
    dag=dag,
)

fetch_teams_task = PythonOperator(
    task_id='fetch_teams',
    python_callable=fetch_teams,
    dag=dag,
)

fetch_players_task = PythonOperator(
    task_id='fetch_players',
    python_callable=fetch_players,
    dag=dag,
)

fetch_games_task = PythonOperator(
    task_id='fetch_games',
    python_callable=fetch_games,
    dag=dag,
)

fetch_player_stats_task = PythonOperator(
    task_id='fetch_stats',
    python_callable=fetch_stats,
    dag=dag,
)

insert_teams_task = PythonOperator(
    task_id='insert_teams',
    python_callable=insert_teams,
    op_args=[fetch_teams_task.output],
    dag=dag,
)

insert_players_task = PythonOperator(
    task_id='insert_players',
    python_callable=insert_players,
    op_args=[fetch_players_task.output],
    dag=dag,
)

insert_games_task = PythonOperator(
    task_id='insert_games',
    python_callable=insert_games,
    op_args=[fetch_games_task.output],
    dag=dag,
)

insert_player_stats_task = PythonOperator(
    task_id='insert_player_stats',
    python_callable=insert_player_stats,
    op_args=[fetch_player_stats_task.output],
    dag=dag,
)




# Define task dependencies
create_tables_task >> fetch_teams_task >> insert_teams_task >> fetch_players_task >> insert_players_task >> fetch_games_task >> insert_games_task >> fetch_player_stats_task >> insert_player_stats_task
