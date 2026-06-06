import streamlit as st
import psycopg2
import pandas as pd
import time

# Page config
st.set_page_config(
    page_title="E-Commerce Analytics",
    page_icon="🛒",
    layout="wide"
)

# Connect to PostgreSQL
def get_connection():
    return psycopg2.connect(
        host="localhost",
        port="5432",
        database="ecommerce",
        user="sanjana",
        password="sanjana123"
    )

# Fetch data from database
def get_orders():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM orders ORDER BY timestamp DESC", conn)
    conn.close()
    return df

def get_kpi():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM kpi_summary ORDER BY id DESC LIMIT 1")
    kpi = cursor.fetchone()
    conn.close()
    return kpi

# Dashboard title
st.title("🛒 Real-Time E-Commerce Analytics Pipeline")
st.markdown("Live dashboard updating every 3 seconds from PostgreSQL")
st.markdown("---")

# Auto refresh every 3 seconds
while True:
    orders_df = get_orders()
    kpi = get_kpi()

    if kpi:
        # KPI metrics row
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("💰 Total Revenue", f"${kpi[2]}")
        col2.metric("📦 Total Orders", kpi[1])
        col3.metric("🏆 Top Product", kpi[3])
        col4.metric("👤 Top Customer", kpi[4])

        st.markdown("---")

        # Charts row
        col5, col6 = st.columns(2)

        with col5:
            st.subheader("📈 Revenue by Product")
            product_df = orders_df.groupby("product")["revenue"].sum().reset_index()
            product_df = product_df.sort_values("revenue", ascending=False)
            st.bar_chart(product_df.set_index("product"))

        with col6:
            st.subheader("👤 Orders by Customer")
            customer_df = orders_df.groupby("customer")["order_id"].count().reset_index()
            customer_df.columns = ["customer", "orders"]
            customer_df = customer_df.sort_values("orders", ascending=False)
            st.bar_chart(customer_df.set_index("customer"))

        st.markdown("---")

        # Recent orders table
        st.subheader("📋 Recent Orders")
        st.dataframe(orders_df.head(10), use_container_width=True)

    time.sleep(3)
    st.rerun()