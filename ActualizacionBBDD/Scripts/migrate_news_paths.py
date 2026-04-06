import psycopg2
from psycopg2 import sql

# Database URLs
LOCAL_URL = "postgresql://space_user:space_password@localhost:5433/space_db"
REMOTE_URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"

def migrate_database(url, label):
    print(f"\n--- Migrating {label} ---")
    try:
        conn = psycopg2.connect(url)
        cur = conn.cursor()
        
        # Select all news items that have the old prefixes
        cur.execute("SELECT id, rutanoticia FROM news WHERE rutanoticia LIKE '/api/v1/news/%' OR rutanoticia LIKE '/api/v1/news_content/%'")
        rows = cur.fetchall()
        
        print(f"Found {len(rows)} items to migrate in {label}.")
        
        updated_count = 0
        for news_id, old_path in rows:
            filename = old_path.split('/')[-1]
            cur.execute("UPDATE news SET rutanoticia = %s WHERE id = %s", (filename, news_id))
            updated_count += 1
            
        conn.commit()
        cur.close()
        conn.close()
        print(f"[OK] {label}: Updated {updated_count} records.")
    except Exception as e:
        print(f"[!] ERROR in {label}: {e}")

if __name__ == "__main__":
    migrate_database(LOCAL_URL, "Local")
    migrate_database(REMOTE_URL, "Remote")
