import psycopg2

LOCAL_URL = "postgresql://space_user:space_password@localhost:5433/space_db"

def check_rockets():
    try:
        conn = psycopg2.connect(LOCAL_URL)
        cur = conn.cursor()
        cur.execute("SELECT id, name, image FROM rockets LIMIT 5;")
        rows = cur.fetchall()
        print("Rockets in DB:")
        for row in rows:
            print(row)
        
        cur.execute("SELECT id, name, image FROM satellites LIMIT 5;")
        rows = cur.fetchall()
        print("\nSatellites in DB:")
        for row in rows:
            print(row)
            
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_rockets()
