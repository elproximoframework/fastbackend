import psycopg2
import json

URL = "postgresql://space_user:space_password@localhost:5433/space_db"

def get_funfacts():
    try:
        conn = psycopg2.connect(URL)
        cur = conn.cursor()
        cur.execute('SELECT id, name, "funFact" FROM satellites ORDER BY id')
        rows = cur.fetchall()
        with open('sat_funfacts.json', 'w', encoding='utf-8') as f:
            data = [{"id": row[0], "name": row[1], "funFact": row[2]} for row in rows]
            json.dump(data, f, indent=2, ensure_ascii=False)
        cur.close()
        conn.close()
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    get_funfacts()
