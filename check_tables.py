import psycopg2
import sys

URL = "postgresql://space_user:space_password@localhost:5433/space_db"

try:
    conn = psycopg2.connect(URL)
    cur = conn.cursor()
    cur.execute("SELECT name, logo FROM companies")
    companies = cur.fetchall()
    print("Companies in DB:")
    for name, logo in companies:
        print(f" - {name}: {logo}")
    conn.close()
except Exception as e:
    print(f"FAILURE: {e}")
    sys.exit(1)
