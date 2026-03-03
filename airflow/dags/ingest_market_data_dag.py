from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

from pipelines.market_snapshot import run_market_snapshot


with DAG(
    dag_id="ingest_market_every_15m",
    start_date=datetime(2026, 1, 1),
    schedule="*/15 * * * *",
    catchup=False,
    tags=["market", "snapshots"],
) as dag:
    snapshot_market = PythonOperator(
        task_id="snapshot_market",
        python_callable=run_market_snapshot,
    )
