"""Main DAG file."""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators import (StageToRedshiftOperator, LoadFactOperator,
                               LoadDimensionOperator, DataQualityOperator)
from helpers import SqlQueries

default_args = {
    'owner': 'jonathankamau',
    'start_date': datetime(2019, 1, 12),
    'depends_on_past': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'email_on_retry': False

}

dag = DAG('udac_example_dag',
          default_args=default_args,
          description='Load and transform data in Redshift with Airflow',
          schedule_interval='0 * * * *',
          catchup=False
          )

start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)

stage_events_to_redshift = StageToRedshiftOperator(
    task_id='Stage_events',
    dag=dag,
    provide_context=True,
    table='staging_events',
    drop_table=True,
    aws_connection_id='aws_credentials',
    redshift_connection_id='redshift',
    create_query=SqlQueries.create_staging_events_table,
    s3_bucket='udacity-dend',
    s3_key='log_data',
    copy_options="json 's3://udacity-dend/log_json_path.json'"
)

stage_songs_to_redshift = StageToRedshiftOperator(
    task_id='Stage_songs',
    dag=dag,
    provide_context=True,
    table='staging_songs',
    drop_table=True,
    aws_connection_id='aws_credentials',
    redshift_connection_id='redshift',
    create_query=SqlQueries.create_staging_songs_table,
    s3_bucket='udacity-dend',
    s3_key='song_data',
    copy_options="json 'auto'"
)

load_songplays_table = LoadFactOperator(
    task_id='Load_songplays_fact_table',
    dag=dag,
    conn_id='redshift',
    target_table='songplays',
    drop_table=True,
    create_query=SqlQueries.create_songplays_table,
    insert_query=SqlQueries.songplay_table_insert,
    append=False
)

load_user_dimension_table = LoadDimensionOperator(
    task_id='Load_user_dim_table',
    dag=dag,
    conn_id='redshift',
    target_table='users',
    drop_table=True,
    create_query=SqlQueries.create_users_table,
    insert_query=SqlQueries.user_table_insert,
    append=False
)

load_song_dimension_table = LoadDimensionOperator(
    task_id='Load_song_dim_table',
    dag=dag,
    conn_id='redshift',
    target_table='songs',
    drop_table=True,
    create_query=SqlQueries.create_songs_table,
    insert_query=SqlQueries.song_table_insert,
    append=False
)

load_artist_dimension_table = LoadDimensionOperator(
    task_id='Load_artist_dim_table',
    dag=dag,
    conn_id='redshift',
    target_table='artists',
    drop_table=True,
    create_query=SqlQueries.create_artist_table,
    insert_query=SqlQueries.artist_table_insert,
    append=False
)

load_time_dimension_table = LoadDimensionOperator(
    task_id='Load_time_dim_table',
    dag=dag,
    conn_id='redshift',
    target_table='time',
    drop_table=True,
    create_query=SqlQueries.create_time_table,
    insert_query=SqlQueries.time_table_insert,
    append=False
)

run_quality_checks = DataQualityOperator(
    task_id='Run_data_quality_checks',
    dag=dag,
    conn_id='redshift',
    target_tables=["songplays", "users", "songs", "artists", "time"],
)

end_operator = DummyOperator(task_id='End_execution',  dag=dag)

start_operator.set_downstream(
    [stage_events_to_redshift, stage_songs_to_redshift])
load_songplays_table.set_upstream(
    [stage_events_to_redshift, stage_songs_to_redshift])
load_songplays_table.set_downstream(
    [load_song_dimension_table, load_user_dimension_table, 
     load_artist_dimension_table, load_time_dimension_table])
run_quality_checks.set_upstream(
    [load_song_dimension_table, load_user_dimension_table,
     load_artist_dimension_table, load_time_dimension_table])
end_operator.set_upstream(run_quality_checks)
