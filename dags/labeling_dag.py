from datetime import datetime, timezone
from airflow import DAG
from airflow.operators.python import PythonOperator

from create_session import create_session

with DAG(
    dag_id = 'create_labeling_session',
    start_date=datetime(2026, 1, 1, tzinfo=timezone.utc),
    schedule="0 20 * * *",
    catchup=False,
    tags = ["surf", "labeling_app"]
) as dag:
 
    create_session_task = PythonOperator(
        task_id = "create_session",
        python_callable = create_session
    )


if __name__ == "__main__":
    dag.test()