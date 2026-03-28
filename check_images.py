import psycopg2

LOCAL_URL = "postgresql://space_user:space_password@localhost:5433/space_db"

def check_images():
    try:
        conn = psycopg2.connect(LOCAL_URL)
        cur = conn.cursor()
        cur.execute("SELECT id, image FROM news;")
        rows = cur.fetchall()
        print("News Images in DB:")
        for row in rows:
            print(row)
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_images()
