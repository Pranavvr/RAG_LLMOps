from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

from pipelines.news_snapshot import run_news_snapshot


with DAG(
    dag_id="ingest_news_daily",
    start_date=datetime(2026, 1, 1),
    schedule="0 6 * * *",
    catchup=False,
    tags=["news", "snapshots"],
) as dag:
    snapshot_news = PythonOperator(
        task_id="snapshot_news",
        python_callable=run_news_snapshot,
    )
