from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timezone

# Config paths
DBT_PROJECT_DIR = "/opt/airflow/dbt"
DBT_PROFILES_DIR = "/opt/airflow/dbt"


from main_ingest import run_ingest
from scoring.simple_model import full_scoring

with DAG(
    dag_id = 'surf_ingest',
    start_date=datetime(2026, 1, 1, tzinfo=timezone.utc),
    schedule="0 11 * * *",
    catchup=False,
    tags=["surf", "ingest"],
) as dag:
    
    ingest_task = PythonOperator(
        task_id = "run_ingest",
        python_callable = run_ingest
    )

    dbt_run = BashOperator(
        task_id = "dbt_run",
        bash_command = f"cd {DBT_PROJECT_DIR} && dbt build --profiles-dir {DBT_PROFILES_DIR}",

    )

    simple_score = PythonOperator(
        task_id = "simple_score",
        python_callable = full_scoring
    )


    # Set task dependencies
    ingest_task >> dbt_run >> simple_score