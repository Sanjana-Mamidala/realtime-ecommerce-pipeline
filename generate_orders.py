import random
import datetime
import time
import json
from kafka import KafkaProducer

# Connect to Kafka
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

# List of fake products in our e-commerce store
products = ["Laptop", "Phone", "Headphones", "Keyboard", "Mouse"]

# List of fake customers
customers = ["Alice", "Bob", "Charlie", "Diana", "Eve"]

# Generate one fake order
def generate_order():
    order = {
        "order_id": random.randint(1000, 9999),
        "customer": random.choice(customers),
        "product": random.choice(products),
        "quantity": random.randint(1, 5),
        "price": round(random.uniform(10.0, 500.0), 2),
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    return order

# Send orders to Kafka continuously
print("🛒 Sending orders to Kafka...\n")

order_count = 0

while True:
    order_count += 1
    order = generate_order()
    producer.send('ecommerce_orders', value=order)
    print(f"✅ Order #{order_count} sent to Kafka: {order['customer']} bought {order['product']} for ${order['price']}")
    time.sleep(2)