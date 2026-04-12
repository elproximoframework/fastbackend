import psycopg2
import sys

# Database URLs
LOCAL_URL = "postgresql://space_user:space_password@localhost:5433/space_db"

def get_companies_in_range(start_id, end_id):
    try:
        conn = psycopg2.connect(LOCAL_URL)
        cur = conn.cursor()
        cur.execute("SELECT id, name, country FROM companies WHERE id BETWEEN %s AND %s ORDER BY id ASC", (start_id, end_id))
        results = cur.fetchall()
        
        if results:
            print(f"--- Companies from ID {start_id} to {end_id} ---")
            for row in results:
                print(f"ID: {row[0]} | Name: {row[1]} | Country: {row[2]}")
        else:
            print(f"[!] No companies found in range {start_id}-{end_id}")
            
        cur.close()
        conn.close()
    except Exception as e:
        print(f"[!] Error: {e}")

if __name__ == "__main__":
    get_companies_in_range(451, 460)
