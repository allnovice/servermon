import streamlit as st
import psycopg2
import pandas as pd

st.set_page_config(page_title="Server Monitor", layout="wide")
st.title("🟢 Server Monitor Dashboard")

try:
    # Connect to DB using Streamlit secrets
    conn_str = st.secrets["NEON_CONN"]
    conn = psycopg2.connect(conn_str)

    # Fetch latest 50 rows ordered by timestamp_local descending
    query = """
        SELECT id, timestamp_local, server_name, status
        FROM server_status
        ORDER BY timestamp_local DESC
        LIMIT 50;
    """
    df = pd.read_sql(query, conn)

    if df.empty:
        st.info("No data in server_status table yet.")
    else:
        # Display the table
        st.subheader("📋 Latest Server Status (Local Time)")
        st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"Database error: {e}")
