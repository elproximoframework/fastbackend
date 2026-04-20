import psycopg2

def check_db():
    conn_str = "postgresql://space_user:space_password@localhost:5433/space_db"
    try:
        conn = psycopg2.connect(conn_str)
        cur = conn.cursor()
        print("--- Duplicates check ---")
        cur.execute("SELECT id, name FROM companies WHERE name ILIKE '%Saudi Space%' OR name ILIKE '%Roketsan%' ORDER BY id")
        rows = cur.fetchall()
        for row in rows:
            print(f"{row[0]}|{row[1]}")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_db()
