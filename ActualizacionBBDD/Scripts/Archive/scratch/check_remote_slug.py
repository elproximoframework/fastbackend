import psycopg2

def check_slug():
    conn_str = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"
    try:
        conn = psycopg2.connect(conn_str)
        cur = conn.cursor()
        cur.execute("SELECT id, name, slug FROM companies WHERE slug = 'zerog-aerospace'")
        rows = cur.fetchall()
        print(f"Conflicts found in remote:")
        for row in rows:
            print(f"ID: {row[0]}, Name: {row[1]}, Slug: {row[2]}")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_slug()
