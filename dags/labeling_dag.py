from datetime import datetime, timezone
from airflow import DAG
from airflow.operators.python import PythonOperator

from create_session import create_session
from daily_labeling_reminder import send_daily_labeling_reminder

with DAG(
    dag_id = 'create_labeling_session',
    start_date=datetime(2026, 1, 1, tzinfo=timezone.utc),
    schedule="0 1 * * *",
    catchup=False,
    tags = ["surf", "labeling_app"]
) as dag:
 
    send_daily_reminder = PythonOperator(
        task_id = "send_reminder",
        python_callable = send_daily_labeling_reminder
    )
