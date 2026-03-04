from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

from pipelines.chroma_index import run_build_chroma_index


with DAG(
    dag_id="build_chroma_index",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["chroma", "fundamentals"],
) as dag:
    build_index = PythonOperator(
        task_id="build_index",
        python_callable=run_build_chroma_index,
        op_kwargs={"rebuild": "{{ dag_run.conf.get('rebuild', false) }}"},
    )
