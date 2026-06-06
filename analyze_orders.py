import csv
from collections import defaultdict  # NEW - a special dictionary

# Read all orders from the CSV file
def read_orders():
    orders = []
    with open("orders.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            orders.append(row)
    return orders

# Calculate KPIs
def analyze_orders(orders):
    total_revenue = 0
    product_sales = defaultdict(float)   # tracks revenue per product
    customer_orders = defaultdict(int)   # tracks order count per customer

    for order in orders:
        price = float(order["price"])
        quantity = int(order["quantity"])
        revenue = price * quantity

        total_revenue += revenue
        product_sales[order["product"]] += revenue
        customer_orders[order["customer"]] += 1

    print("=" * 40)
    print("   📊 E-COMMERCE ANALYTICS REPORT")
    print("=" * 40)

    print(f"\n💰 Total Revenue: ${round(total_revenue, 2)}")
    print(f"📦 Total Orders: {len(orders)}")

    print("\n🏆 Revenue by Product:")
    for product, revenue in sorted(product_sales.items(), key=lambda x: x[1], reverse=True):
        print(f"   {product}: ${round(revenue, 2)}")

    print("\n👤 Orders by Customer:")
    for customer, count in sorted(customer_orders.items(), key=lambda x: x[1], reverse=True):
        print(f"   {customer}: {count} orders")

    print("=" * 40)

# Run the analysis
orders = read_orders()
analyze_orders(orders)