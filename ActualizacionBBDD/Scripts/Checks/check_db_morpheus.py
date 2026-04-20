import psycopg2

def check_morpheus():
    conn_str = "postgresql://space_user:space_password@localhost:5433/space_db"
    try:
        conn = psycopg2.connect(conn_str)
        cur = conn.cursor()
        cur.execute("SELECT id, name, slug FROM companies WHERE name ILIKE '%Morpheus%'")
        rows = cur.fetchall()
        print(f"Companies with 'Morpheus' in name:")
        for row in rows:
            print(f"ID: {row[0]}, Name: {row[1]}, Slug: {row[2]}")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_morpheus()
