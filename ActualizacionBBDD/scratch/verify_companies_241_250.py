import psycopg2

# Database URLs
LOCAL_URL = "postgresql://space_user:space_password@localhost:5433/space_db"
REMOTE_URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"

def verify_updates(start_id, end_id):
    """
    Verify that the companies in the specified ID range have been updated.
    Checks for the 'description' field to ensure enrichment.
    """
    for label, url in [("Local", LOCAL_URL), ("Remote", REMOTE_URL)]:
        print(f"--- Verifying {label} (IDs {start_id} to {end_id}) ---")
        try:
            conn = psycopg2.connect(url)
            cur = conn.cursor()
            cur.execute("SELECT id, name, LEFT(description, 50) FROM companies WHERE id BETWEEN %s AND %s ORDER BY id", (start_id, end_id))
            results = cur.fetchall()
            
            if results:
                for row in results:
                    print(f"ID: {row[0]} | Name: {row[1]} | Desc: {row[2]}...")
            else:
                print(f"[!] No companies found in range {start_id}-{end_id}")
                
            cur.close()
            conn.close()
        except Exception as e:
            print(f"[!] Error in {label}: {e}")

if __name__ == "__main__":
    verify_updates(241, 250)
