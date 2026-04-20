import psycopg2

LOCAL_URL = "postgresql://space_user:space_password@localhost:5433/space_db"
REMOTE_URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"

def verify(url, label):
    try:
        conn = psycopg2.connect(url)
        cur = conn.cursor()
        cur.execute("SELECT name FROM companies WHERE name IN ('SpaceX', 'Blue Origin', 'PLD Space')")
        names = [r[0] for r in cur.fetchall()]
        print(f"{label}: {names}")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"{label} failed: {e}")

if __name__ == "__main__":
    verify(LOCAL_URL, "Local")
    verify(REMOTE_URL, "Remote")
