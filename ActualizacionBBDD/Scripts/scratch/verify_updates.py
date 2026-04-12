import psycopg2

LOCAL_URL = "postgresql://space_user:space_password@localhost:5433/space_db"

def verify_updates(ids):
    try:
        conn = psycopg2.connect(LOCAL_URL)
        cur = conn.cursor()
        for id in ids:
            cur.execute("SELECT id, name, description, ceo, sector FROM companies WHERE id = %s", (id,))
            row = cur.fetchone()
            if row:
                print(f"ID: {row[0]}")
                print(f"Name: {row[1]}")
                print(f"CEO: {row[3]}")
                print(f"Sector: {row[4]}")
                print(f"Description (Start): {row[2][:100]}...")
                print("-" * 20)
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    verify_updates([471, 480])
