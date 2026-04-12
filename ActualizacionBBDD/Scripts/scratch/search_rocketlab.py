import psycopg2

def search_companies(query):
    conn_str = "postgresql://space_user:space_password@localhost:5433/space_db"
    try:
        conn = psycopg2.connect(conn_str)
        cur = conn.cursor()
        cur.execute("SELECT id, name FROM companies WHERE name ILIKE %s", (f"%{query}%",))
        rows = cur.fetchall()
        print(f"Results for '{query}':")
        for row in rows:
            print(f"{row[0]}|{row[1]}")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    search_companies("Rocket Lab")
