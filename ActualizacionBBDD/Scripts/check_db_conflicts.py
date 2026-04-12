import psycopg2

def check_conflicts():
    conn_str = "postgresql://space_user:space_password@localhost:5433/space_db"
    try:
        conn = psycopg2.connect(conn_str)
        cur = conn.cursor()
        names = ['Mynaric', 'Myriota', 'Momentus', 'Moog', 'Motiv', 'mPower', 'Muon', 'Nanoracks', 'Ames']
        query = "SELECT id, name, slug FROM companies WHERE " + " OR ".join([f"name ILIKE '%{n}%'" for n in names])
        cur.execute(query)
        rows = cur.fetchall()
        print(f"Potential conflicts:")
        for row in rows:
            print(f"ID: {row[0]}, Name: {row[1]}, Slug: {row[2]}")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_conflicts()
