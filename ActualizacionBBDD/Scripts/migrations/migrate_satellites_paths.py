import psycopg2
from psycopg2 import sql

# Database URLs
LOCAL_URL = "postgresql://space_user:space_password@localhost:5433/space_db"
REMOTE_URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"

def migrate_database(url, label):
    print(f"\n--- Migrating Satellites in {label} ---")
    try:
        conn = psycopg2.connect(url)
        cur = conn.cursor()
        
        # 1. Check for records with legacy prefix
        cur.execute("SELECT id, name, image FROM satellites WHERE image LIKE '/api/v1/satellite_images/%'")
        rows = cur.fetchall()
        print(f"Found {len(rows)} satellites to migrate in {label}.")
        
        for sat_id, name, old_path in rows:
            filename = old_path.split('/')[-1]
            print(f"  Cleaning {name}: {old_path} -> {filename}")
            cur.execute("UPDATE satellites SET image = %s WHERE id = %s", (filename, sat_id))
            
        conn.commit()
        cur.close()
        conn.close()
        print(f"[OK] {label}: Satellite migration completed.")
    except Exception as e:
        print(f"[!] ERROR in {label}: {e}")

if __name__ == "__main__":
    migrate_database(LOCAL_URL, "Local")
    migrate_database(REMOTE_URL, "Remote")
