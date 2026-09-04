from datetime import datetime, timezone
from airflow import DAG
from airflow.operators.python import PythonOperator

from llm_summary_generation import generate_summary_output


with DAG (
    dag_id = 'generate_llm_forecast',
    start_date=datetime(2026, 1, 1, tzinfo=timezone.utc),
    schedule="0 18 * * 0",
    catchup=False,
    tags = ["surf", "ai_summary"]
) as dag:

    generate_llm_sumary = PythonOperator(
        task_id = 'generate_llm_summary',
        python_callable = generate_summary_output
    )

