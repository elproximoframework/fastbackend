import psycopg2
import json

URL = "postgresql://space_user:space_password@localhost:5433/space_db"

def get_companies():
    try:
        conn = psycopg2.connect(URL)
        cur = conn.cursor()
        cur.execute("SELECT id, name, country FROM companies WHERE id BETWEEN 381 AND 390 ORDER BY id;")
        rows = cur.fetchall()
        companies = []
        for row in rows:
            companies.append({"id": row[0], "name": row[1], "country": row[2]})
        print(json.dumps(companies, indent=2))
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_companies()
