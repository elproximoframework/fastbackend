import psycopg2
import json

URL = "postgresql://space_user:space_password@localhost:5433/space_db"

def get_funfacts():
    try:
        conn = psycopg2.connect(URL)
        cur = conn.cursor()
        cur.execute('SELECT name, "funFact" FROM satellites')
        rows = cur.fetchall()
        data = {row[0]: row[1] for row in rows}
        print(json.dumps(data, indent=2, ensure_ascii=False))
        cur.close()
        conn.close()
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    get_funfacts()
