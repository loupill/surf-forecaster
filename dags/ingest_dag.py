from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timezone

import sys
sys.path.insert(0, '../src')
from main_ingest import run_ingest

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