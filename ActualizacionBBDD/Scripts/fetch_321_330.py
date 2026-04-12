import psycopg2

def get_companies():
    conn_str = "postgresql://space_user:space_password@localhost:5433/space_db"
    try:
        conn = psycopg2.connect(conn_str)
        cur = conn.cursor()
        cur.execute("SELECT id, name, country FROM companies WHERE id >= 321 AND id <= 330 ORDER BY id")
        rows = cur.fetchall()
        for row in rows:
            print(f"{row[0]}|{row[1]}|{row[2]}")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_companies()
