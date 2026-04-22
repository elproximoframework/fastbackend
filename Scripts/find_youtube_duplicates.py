import psycopg2

LOCAL_URL = "postgresql://space_user:space_password@localhost:5433/space_db"

def find_duplicates():
    try:
        conn = psycopg2.connect(LOCAL_URL)
        cur = conn.cursor()
        cur.execute("SELECT url, COUNT(*) FROM youtube GROUP BY url HAVING COUNT(*) > 1")
        dupes = cur.fetchall()
        if dupes:
            print("Found duplicates:")
            for d in dupes:
                print(f"URL: {d[0]} - Count: {d[1]}")
        else:
            print("No duplicates found.")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    find_duplicates()
