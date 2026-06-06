import psycopg2

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="ecommerce",
    user="sanjana",
    password="sanjana123"
)

cursor = conn.cursor()

# Create orders table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id SERIAL PRIMARY KEY,
        order_id INTEGER,
        customer VARCHAR(100),
        product VARCHAR(100),
        quantity INTEGER,
        price FLOAT,
        revenue FLOAT,
        timestamp TIMESTAMP
    )
""")

# Create KPI summary table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS kpi_summary (
        id SERIAL PRIMARY KEY,
        total_orders INTEGER,
        total_revenue FLOAT,
        top_product VARCHAR(100),
        top_customer VARCHAR(100),
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

conn.commit()
cursor.close()
conn.close()

print("✅ Database tables created successfully!")