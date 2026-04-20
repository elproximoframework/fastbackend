import psycopg2
import sys

URL = "postgresql://space_user:space_password@localhost:5433/space_db"

def get_companies():
    try:
        conn = psycopg2.connect(URL)
        cur = conn.cursor()
        cur.execute("SELECT id, name, country FROM companies WHERE id BETWEEN 391 AND 400 ORDER BY id;")
        rows = cur.fetchall()
        for row in rows:
            print(f"{row[0]}|{row[1]}|{row[2]}")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    get_companies()
