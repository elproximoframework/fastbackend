import psycopg2

LOCAL_URL = "postgresql://space_user:space_password@localhost:5433/space_db"

def list_constraints():
    try:
        conn = psycopg2.connect(LOCAL_URL)
        cur = conn.cursor()
        cur.execute("""
            SELECT conname, pg_get_constraintdef(c.oid)
            FROM pg_constraint c
            JOIN pg_namespace n ON n.oid = c.connamespace
            WHERE n.nspname = 'public' AND conrelid = 'youtube'::regclass;
        """)
        constraints = cur.fetchall()
        for con in constraints:
            print(f"Constraint: {con[0]} -> {con[1]}")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    list_constraints()
