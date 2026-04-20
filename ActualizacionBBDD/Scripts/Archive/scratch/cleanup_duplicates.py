import psycopg2

def cleanup(url, label):
    print(f"Cleaning up {label}...")
    try:
        conn = psycopg2.connect(url)
        cur = conn.cursor()
        cur.execute("DELETE FROM companies WHERE id >= 609")
        print(f"Deleted {cur.rowcount} rows from {label}")
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error in {label}: {e}")

if __name__ == "__main__":
    LOCAL_URL = "postgresql://space_user:space_password@localhost:5433/space_db"
    REMOTE_URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"
    cleanup(LOCAL_URL, "Local")
    cleanup(REMOTE_URL, "Remote")
