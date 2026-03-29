import psycopg2
import sys

# Testing with original credentials but explicitly on localhost (could be IPv6)
URL = "postgresql://space_user:space_password@localhost:5433/space_db"

try:
    conn = psycopg2.connect(URL)
    print("SUCCESS: Connected to PostgreSQL on port 5433")
    conn.close()
except Exception as e:
    print(f"FAILURE: {e}")
    sys.exit(1)
