import os
import psycopg2
from datetime import datetime
import requests

# ------------------- Configuration -------------------
# If running outside Streamlit, you can export NEON_CONN as an env variable:
# export NEON_CONN="your_connection_string"
conn_str = os.getenv("NEON_CONN")  # or use st.secrets["NEON_CONN"] if in Streamlit
servers = [
    {"name": "Users API", "url": "http://192.168.100.72:3001/users"},
    {"name": "CMMS Dashboard", "url": "https://related-certain-frog.ngrok-free.app"}
]

# ------------------- DB Connection -------------------
conn = psycopg2.connect(conn_str)
cursor = conn.cursor()

# ------------------- Monitoring Loop -------------------
for server in servers:
    try:
        resp = requests.get(server["url"], timeout=10)
        status = "UP" if resp.status_code == 200 else "DOWN"
    except requests.RequestException:
        status = "DOWN"

    timestamp = datetime.utcnow()
    cursor.execute(
        """
        INSERT INTO server_status (server_name, status, checked_at)
        VALUES (%s, %s, %s)
        """,
        (server["name"], status, timestamp)
    )
    print(f"[{timestamp}] {server['name']} -> {status}")

# Commit and close
conn.commit()
cursor.close()
conn.close()
