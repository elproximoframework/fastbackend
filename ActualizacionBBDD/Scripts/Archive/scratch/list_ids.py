import psycopg2

LOCAL_URL = "postgresql://space_user:space_password@localhost:5433/space_db"

def list_ids(start, end):
    try:
        conn = psycopg2.connect(LOCAL_URL)
        cur = conn.cursor()
        cur.execute("SELECT id, name, country FROM companies WHERE id BETWEEN %s AND %s ORDER BY id", (start, end))
        results = cur.fetchall()
        for row in results:
            print(f"{row[0]}|{row[1]}|{row[2]}")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    list_ids(471, 480)
