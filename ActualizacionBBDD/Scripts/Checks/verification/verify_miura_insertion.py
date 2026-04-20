import psycopg2

LOCAL_URL = "postgresql://space_user:space_password@localhost:5433/space_db"
REMOTE_URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"

def verify_miura(url, name):
    try:
        conn = psycopg2.connect(url)
        cur = conn.cursor()
        cur.execute("SELECT id, name, manufacturer_id, status FROM rockets WHERE name LIKE %s", ('Miura%',))
        rows = cur.fetchall()
        print(f"--- Verification for Miura in {name} ---")
        if not rows:
            print("No Miura rockets found.")
        for row in rows:
            print(f"ID: {row[0]} | Name: {row[1]} | Manufacturer: {row[2]} | Status: {row[3]}")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error in {name}: {e}")

if __name__ == "__main__":
    verify_miura(LOCAL_URL, "LOCAL")
    verify_miura(REMOTE_URL, "REMOTE")
