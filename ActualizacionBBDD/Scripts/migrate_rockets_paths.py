import psycopg2
from psycopg2 import sql

# Database URLs
LOCAL_URL = "postgresql://space_user:space_password@localhost:5433/space_db"
REMOTE_URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"

def migrate_database(url, label):
    print(f"\n--- Migrating Rockets in {label} ---")
    try:
        conn = psycopg2.connect(url)
        cur = conn.cursor()
        
        # 1. Check for records with legacy prefix
        cur.execute("SELECT id, name, image FROM rockets WHERE image LIKE '/api/v1/rocket_images/%'")
        rows = cur.fetchall()
        print(f"Found {len(rows)} rockets to migrate in {label}.")
        
        for rocket_id, name, old_path in rows:
            filename = old_path.split('/')[-1]
            print(f"  Cleaning {name}: {old_path} -> {filename}")
            cur.execute("UPDATE rockets set image = %s WHERE id = %s", (filename, rocket_id))
            
        conn.commit()
        cur.close()
        conn.close()
        print(f"[OK] {label}: Rocket migration completed.")
    except Exception as e:
        print(f"[!] ERROR in {label}: {e}")

if __name__ == "__main__":
    migrate_database(LOCAL_URL, "Local")
    migrate_database(REMOTE_URL, "Remote")
