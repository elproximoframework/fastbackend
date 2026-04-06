import psycopg2

# Database URLs
LOCAL_URL = "postgresql://space_user:space_password@localhost:5433/space_db"
REMOTE_URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"

def verify(url, label):
    try:
        conn = psycopg2.connect(url)
        cur = conn.cursor()
        cur.execute("SELECT count(*) FROM news WHERE rutanoticia LIKE '/api/v1/news/%'")
        count = cur.fetchone()[0]
        cur.execute("SELECT count(*) FROM news")
        total = cur.fetchone()[0]
        cur.execute("SELECT rutanoticia FROM news LIMIT 1")
        sample = cur.fetchone()[0]
        print(f"{label}: {count} with prefix, {total} total. Sample: {sample}")
        conn.close()
    except Exception as e:
        print(f"Error {label}: {e}")

if __name__ == "__main__":
    verify(LOCAL_URL, "Local")
    verify(REMOTE_URL, "Remote")
