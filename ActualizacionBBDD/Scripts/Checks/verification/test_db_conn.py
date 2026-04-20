import psycopg2
import sys

URL = "postgresql://space_user:space_password@localhost:5432/space_db"

try:
    conn = psycopg2.connect(URL)
    print("SUCCESS: Connected to PostgreSQL on port 5432")
    conn.close()
except Exception as e:
    print(f"FAILURE: {e}")
    sys.exit(1)
