import psycopg2

URL = "postgresql://space_user:space_password@localhost:5433/space_db"

def get_funfacts():
    try:
        conn = psycopg2.connect(URL)
        cur = conn.cursor()
        cur.execute('SELECT id, name, "funFact" FROM satellites')
        rows = cur.fetchall()
        for row in rows:
            print(f"ID: {row[0]}, Name: {row[1]}, FunFact: {row[2]}")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    get_funfacts()
