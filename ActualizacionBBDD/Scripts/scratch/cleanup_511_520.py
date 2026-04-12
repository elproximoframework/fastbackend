import psycopg2

LOCAL_URL = "postgresql://space_user:space_password@localhost:5433/space_db"
REMOTE_URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"

def cleanup(url, label):
    print(f"--- Cleaning up {label} ---")
    try:
        conn = psycopg2.connect(url)
        cur = conn.cursor()
        
        # 1. Delete accidental inserts (based on the names I used in the JSON)
        cur.execute("DELETE FROM companies WHERE id >= 600 AND (name = 'Saudi Space Agency (SSA)' OR name = 'Roketsan')")
        print(f"Deleted accidental inserts in {label}: {cur.rowcount}")
        
        # 2. Rename existing records to match the enriched names
        cur.execute("UPDATE companies SET name = 'Saudi Space Agency (SSA)' WHERE id = 518")
        cur.execute("UPDATE companies SET name = 'Roketsan' WHERE id = 520")
        print(f"Renamed records 518 and 520 in {label}")
        
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error in {label}: {e}")

if __name__ == "__main__":
    cleanup(LOCAL_URL, "Local")
    cleanup(REMOTE_URL, "Remote")
