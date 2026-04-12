import psycopg2

# Database URLs
LOCAL_URL = "postgresql://space_user:space_password@localhost:5433/space_db"
REMOTE_URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"

def get_companies_in_range(start_id, end_id):
    """
    Search for companies' names and countries in the specified ID range.
    """
    url = REMOTE_URL # Checking remote as it usually has the authoritative list
    print(f"--- Checking IDs {start_id} to {end_id} ---")
    try:
        conn = psycopg2.connect(url)
        cur = conn.cursor()
        cur.execute("SELECT id, name, country FROM companies WHERE id BETWEEN %s AND %s ORDER BY id", (start_id, end_id))
        results = cur.fetchall()
        
        if results:
            for row in results:
                print(f"{row[0]}|{row[1]}|{row[2]}")
        else:
            print(f"[!] No companies found in range {start_id}-{end_id}")
            
        cur.close()
        conn.close()
    except Exception as e:
        print(f"[!] Error: {e}")

if __name__ == "__main__":
    get_companies_in_range(241, 250)
