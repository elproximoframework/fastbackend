import psycopg2
import sys

# Testing with credentials from instalaciondockerypostgresql.md
URL = "postgresql://admin:123456@localhost:5432/midb"

try:
    conn = psycopg2.connect(URL)
    print("SUCCESS: Connected to PostgreSQL on port 5432 with admin credentials")
    conn.close()
except Exception as e:
    print(f"FAILURE: {e}")
    sys.exit(1)
