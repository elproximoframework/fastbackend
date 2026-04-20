import psycopg2

def check_rocket_labs():
    conn_str = "postgresql://space_user:space_password@localhost:5433/space_db"
    try:
        conn = psycopg2.connect(conn_str)
        cur = conn.cursor()
        print("--- Checking Rocket Lab entries ---")
        cur.execute("SELECT id, name, country FROM companies WHERE name ILIKE '%Rocket Lab%' ORDER BY id")
        rows = cur.fetchall()
        for row in rows:
            print(f"{row[0]}|{row[1]}|{row[2]}")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_rocket_labs()
