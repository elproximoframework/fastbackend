import psycopg2

def fetch_batch():
    conn_str = "postgresql://space_user:space_password@localhost:5433/space_db"
    try:
        conn = psycopg2.connect(conn_str)
        cur = conn.cursor()
        cur.execute("SELECT id, name FROM companies WHERE id >= 441 AND id <= 450 ORDER BY id")
        results = cur.fetchall()
        for row in results:
            print(f"ID: {row[0]}, Name: {row[1]}")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fetch_batch()
