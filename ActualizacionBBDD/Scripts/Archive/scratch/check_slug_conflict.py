import psycopg2

def check_slug(slug):
    conn_str = "postgresql://space_user:space_password@localhost:5433/space_db"
    try:
        conn = psycopg2.connect(conn_str)
        cur = conn.cursor()
        cur.execute("SELECT id, name, slug FROM companies WHERE slug = %s", (slug,))
        row = cur.fetchone()
        if row:
            print(f"ID: {row[0]}, Name: {row[1]}, Slug: {row[2]}")
        else:
            print("No conflicting slug found.")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_slug("ramon-space")
