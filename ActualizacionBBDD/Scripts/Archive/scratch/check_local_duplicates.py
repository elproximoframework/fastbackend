import psycopg2

def check_duplicates():
    conn_str = "postgresql://space_user:space_password@localhost:5433/space_db"
    try:
        conn = psycopg2.connect(conn_str)
        cur = conn.cursor()
        names = ['ZeroG Aerospace (ZeroG Lab)', 'Chuangxing Space (Innovation Academy for Microsatellites of CAS)', 'USPACE Technology Group']
        for name in names:
            cur.execute("SELECT id, name FROM companies WHERE name = %s", (name,))
            rows = cur.fetchall()
            for row in rows:
                print(f"Found duplicate in local: ID: {row[0]}, Name: {row[1]}")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_duplicates()
