import os
import sys
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

# Указываем жесткий путь к нашей новой папке с утилитами внутри Docker
sys.path.append('/opt/airflow/dags/utils')

# Импортируем функцию напрямую из модуля utils
from pipeline import run_etl_pipeline

default_args = {
    'owner': 'alex_de',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    'crypto_data_pipeline_moex_yahoo',
    default_args=default_args,
    description='Пайплайн для сбора котировок BTC и ETH с Yahoo Finance',
    schedule_interval=None,
    catchup=False,
    is_paused_upon_creation=False,
    tags=['crypto', 'junior_project'],
) as dag:

    run_etl_task = PythonOperator(
        task_id='run_crypto_etl',
        python_callable=run_etl_pipeline
    )

    run_etl_task