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

# Check orders table
print("📦 ORDERS IN DATABASE:")
print("=" * 50)
cursor.execute("SELECT * FROM orders ORDER BY id DESC LIMIT 5")
orders = cursor.fetchall()
for order in orders:
    print(order)

# Check KPI summary
print("\n📊 LATEST KPI SUMMARY:")
print("=" * 50)
cursor.execute("SELECT * FROM kpi_summary ORDER BY id DESC LIMIT 1")
kpi = cursor.fetchone()
print(f"Total Orders   : {kpi[1]}")
print(f"Total Revenue  : ${kpi[2]}")
print(f"Top Product    : {kpi[3]}")
print(f"Top Customer   : {kpi[4]}")
print(f"Last Updated   : {kpi[5]}")

cursor.close()
conn.close()