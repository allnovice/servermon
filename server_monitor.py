import streamlit as st
import psycopg2
from psycopg2 import sql

st.set_page_config(page_title="Server Monitor", layout="wide")
st.title("🟢 Server Monitor Dashboard")

try:
    conn_str = st.secrets["NEON_CONN"]
    conn = psycopg2.connect(conn_str)
    cur = conn.cursor()

    cur.execute("SELECT * FROM server_status ORDER BY checked_at DESC LIMIT 50;")
    rows = cur.fetchall()

    if not rows:
        st.info("No data in server_status table yet.")
    else:
        st.dataframe(rows)

except Exception as e:
    st.error(f"Database error: {e}")
