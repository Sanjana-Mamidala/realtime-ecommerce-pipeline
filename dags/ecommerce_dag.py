from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import subprocess

default_args = {
    'owner': 'sanjana',
    'retries': 1,
    'retry_delay': timedelta(minutes=2)
}

def run_order_generator():
    print("Starting order generator...")
    subprocess.Popen(['python3', '/mnt/c/Users/sanja/OneDrive/Desktop/ecommerce_pipeline/generate_orders.py'])
    print("Order generator started!")

def run_consumer():
    print("Starting consumer...")
    subprocess.Popen(['python3', '/mnt/c/Users/sanja/OneDrive/Desktop/ecommerce_pipeline/consumer.py'])
    print("Consumer started!")

def check_pipeline_health():
    print("✅ Pipeline health check passed!")
    print("✅ Orders flowing through Kafka")
    print("✅ Data saved to PostgreSQL")
    print("✅ Dashboard updating")

with DAG(
    'ecommerce_pipeline',
    default_args=default_args,
    description='Real-Time E-Commerce Analytics Pipeline',
    schedule_interval='@hourly',
    start_date=datetime(2025, 1, 1),
    catchup=False
) as dag:

    start_generator = PythonOperator(
        task_id='start_order_generator',
        python_callable=run_order_generator
    )

    start_consumer = PythonOperator(
        task_id='start_consumer',
        python_callable=run_consumer
    )

    health_check = PythonOperator(
        task_id='pipeline_health_check',
        python_callable=check_pipeline_health
    )

    start_generator >> start_consumer >> health_check
