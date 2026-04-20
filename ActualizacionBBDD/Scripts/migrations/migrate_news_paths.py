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
        
        # 1. Migrate regular news
        cur.execute("SELECT id, rutanoticia FROM news WHERE rutanoticia LIKE '/api/v1/news/%' OR rutanoticia LIKE '/api/v1/news_content/%'")
        rows = cur.fetchall()
        print(f"Found {len(rows)} regular news items to migrate in {label}.")
        for news_id, old_path in rows:
            filename = old_path.split('/')[-1]
            cur.execute("UPDATE news SET rutanoticia = %s WHERE id = %s", (filename, news_id))
            
        # 2. Migrate SpaceX news
        cur.execute("SELECT id, rutanoticia FROM newsspacex WHERE rutanoticia LIKE '/api/v1/newsspacex_content/%'")
        rows_sx = cur.fetchall()
        print(f"Found {len(rows_sx)} SpaceX news items to migrate in {label}.")
        for news_id, old_path in rows_sx:
            filename = old_path.split('/')[-1]
            cur.execute("UPDATE newsspacex SET rutanoticia = %s WHERE id = %s", (filename, news_id))
            
        conn.commit()
        cur.close()
        conn.close()
        print(f"[OK] {label}: Migration completed.")
    except Exception as e:
        print(f"[!] ERROR in {label}: {e}")

if __name__ == "__main__":
    migrate_database(LOCAL_URL, "Local")
    migrate_database(REMOTE_URL, "Remote")
