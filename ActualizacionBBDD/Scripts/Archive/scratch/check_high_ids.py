import psycopg2

def check_all_duplicates():
    conn_str = "postgresql://space_user:space_password@localhost:5433/space_db"
    try:
        conn = psycopg2.connect(conn_str)
        cur = conn.cursor()
        cur.execute("SELECT id, name, slug FROM companies WHERE id >= 610 ORDER BY id")
        results = cur.fetchall()
        print(f"Entities with ID >= 610: {results}")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_all_duplicates()
