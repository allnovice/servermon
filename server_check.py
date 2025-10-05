# server_check.py
import os
import psycopg2
import requests
from datetime import datetime

# 1️⃣ Read connection string from env (GitHub Actions will set it)
conn_str = os.environ.get("NEON_CONN")
if not conn_str:
    raise ValueError("NEON_CONN not found in environment variables")

# 2️⃣ Connect to Neon
conn = psycopg2.connect(conn_str)
cur = conn.cursor()

# 3️⃣ Define API to check
API_URL = "https://related-certain-frog.ngrok-free.app/users"
server_name = "Users API"

# 4️⃣ Ping the server
try:
    r = requests.get(API_URL, timeout=10)
    status = "UP" if r.status_code == 200 else "DOWN"
except Exception:
    status = "DOWN"

# 5️⃣ Insert status into server_status table
timestamp = datetime.now().isoformat()

cur.execute(
    """
    INSERT INTO server_status (server_name, status, checked_at)
    VALUES (%s, %s, %s)
    """,
    (server_name, status, timestamp)
)

conn.commit()
cur.close()
conn.close()

print(f"{server_name} is {status} at {timestamp}")
