import psycopg2

def check_slugs():
    conn_str = "postgresql://space_user:space_password@localhost:5433/space_db"
    try:
        conn = psycopg2.connect(conn_str)
        cur = conn.cursor()
        cur.execute("SELECT slug FROM companies WHERE slug LIKE '%ispace%'")
        rows = cur.fetchall()
        for row in rows:
            print(row[0])
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_slugs()
