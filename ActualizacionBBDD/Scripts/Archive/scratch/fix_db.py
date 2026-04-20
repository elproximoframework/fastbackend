import psycopg2

LOCAL_URL = "postgresql://space_user:space_password@localhost:5433/space_db"
REMOTE_URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"

def fix_db(url, label):
    print(f"--- Fixing {label} ---")
    try:
        conn = psycopg2.connect(url)
        cur = conn.cursor()
        
        # 1. Delete mistaken duplicates
        cur.execute("DELETE FROM companies WHERE id IN (614, 615)")
        print(f"Deleted IDs 614, 615 from {label}")
        
        # 2. Rename original rows to match improved names in JSON
        cur.execute("UPDATE companies SET name = 'Vasundharaa Geo Technologies' WHERE id = 453")
        cur.execute("UPDATE companies SET name = 'VestaSpace Technology' WHERE id = 459")
        print(f"Updated names for IDs 453, 459 in {label}")
        
        conn.commit()
        cur.close()
        conn.close()
        print(f"Done fixing {label}.")
    except Exception as e:
        print(f"Error in {label}: {e}")

if __name__ == "__main__":
    fix_db(LOCAL_URL, "Local")
    fix_db(REMOTE_URL, "Remote")
