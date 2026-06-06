import json
import psycopg2
from kafka import KafkaConsumer
from collections import defaultdict
import datetime

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="ecommerce",
    user="sanjana",
    password="sanjana123"
)
cursor = conn.cursor()

# Connect to Kafka
consumer = KafkaConsumer(
    'ecommerce_orders',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    auto_offset_reset='latest',
    group_id='ecommerce_group3'
)

# KPI trackers
total_revenue = 0
total_orders = 0
product_revenue = defaultdict(float)
customer_orders = defaultdict(int)

print("📊 Live KPI Dashboard — Saving to PostgreSQL...\n")
print("=" * 45)

for message in consumer:
    order = message.value
    revenue = round(order['price'] * order['quantity'], 2)

    # Update KPI trackers
    total_revenue += revenue
    total_orders += 1
    product_revenue[order['product']] += revenue
    customer_orders[order['customer']] += 1

    top_product = max(product_revenue, key=product_revenue.get)
    top_customer = max(customer_orders, key=customer_orders.get)

    # Save order to PostgreSQL
    cursor.execute("""
        INSERT INTO orders (order_id, customer, product, quantity, price, revenue, timestamp)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        order['order_id'],
        order['customer'],
        order['product'],
        order['quantity'],
        order['price'],
        revenue,
        order['timestamp']
    ))

    # Save KPI summary to PostgreSQL
    cursor.execute("""
        INSERT INTO kpi_summary (total_orders, total_revenue, top_product, top_customer)
        VALUES (%s, %s, %s, %s)
    """, (
        total_orders,
        round(total_revenue, 2),
        top_product,
        top_customer
    ))

    conn.commit()

    # Print live dashboard
    print(f"\n🛒 Order #{total_orders} — {order['customer']} bought {order['product']}")
    print(f"💰 Total Revenue   : ${round(total_revenue, 2)}")
    print(f"📦 Total Orders    : {total_orders}")
    print(f"🏆 Top Product     : {top_product} (${round(product_revenue[top_product], 2)})")
    print(f"👤 Top Customer    : {top_customer} ({customer_orders[top_customer]} orders)")
    print(f"💾 Saved to PostgreSQL ✅")
    print("-" * 45)