# Real-Time E-Commerce Analytics Pipeline

A production-grade real-time data pipeline built with Python, Apache Kafka, PostgreSQL, Apache Airflow, and Streamlit.

## Architecture

Order Generator → Apache Kafka → Consumer → PostgreSQL → Streamlit Dashboard
↑
Apache Airflow (Orchestration)

## Tech Stack
- **Python** — Data generation and processing
- **Apache Kafka** — Real-time message streaming
- **PostgreSQL** — Data warehouse storage
- **Apache Airflow** — Pipeline orchestration and scheduling
- **Streamlit** — Live analytics dashboard
- **Docker** — Containerization

## Features
- Generates real-time e-commerce orders every 2 seconds
- Streams orders through Kafka message broker
- Calculates live KPIs: revenue, top products, best customers
- Stores all data permanently in PostgreSQL
- Displays live dashboard updating every 3 seconds
- Fully automated with Apache Airflow scheduling

## How to Run

### Step 1: Start Docker services (Kafka, PostgreSQL, Kafka UI)
docker-compose up -d

### Step 2: Set up the database (only first time)
python setup_database.py

### Step 3: Start order generator (Terminal 1)
python generate_orders.py

### Step 4: Start consumer (Terminal 2)
python consumer.py

### Step 5: Launch dashboard (Terminal 3)
streamlit run dashboard.py

### Step 6: Start Airflow (in Ubuntu terminal)
source airflow-env310/bin/activate
export AIRFLOW_HOME=~/airflow
airflow webserver --port 8081

### View dashboards
- **Streamlit Dashboard:** http://localhost:8501
- **Kafka UI:** http://localhost:8080
- **Airflow:** http://localhost:8081

