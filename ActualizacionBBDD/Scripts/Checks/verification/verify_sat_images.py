import psycopg2

URL = "postgresql://space_user:space_password@localhost:5433/space_db"

def check_sat_images():
    try:
        conn = psycopg2.connect(URL)
        cur = conn.cursor()
        cur.execute("SELECT name, image FROM satellites LIMIT 20;")
        rows = cur.fetchall()
        print("Satellite Images in DB:")
        for row in rows:
            print(f"Name: {row[0]}, Image: {row[1]}")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_sat_images()
