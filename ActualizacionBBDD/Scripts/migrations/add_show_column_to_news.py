import psycopg2
import os

# Connection URLs
LOCAL_URL = "postgresql://space_user:space_password@localhost:5433/space_db"
REMOTE_URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"

def run_migration(url, name):
    print(f"\n--- Migrating {name} Database ---")
    try:
        conn = psycopg2.connect(url)
        conn.autocommit = True
        cur = conn.cursor()

        # Check if 'show' column exists in 'news' table
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='news' AND column_name='show';
        """)
        
        if not cur.fetchone():
            print(f"Adding 'show' column to 'news' table in {name}...")
            cur.execute('ALTER TABLE news ADD COLUMN "show" BOOLEAN DEFAULT TRUE;')
            # Update existing records to TRUE (though DEFAULT TRUE usually handles this in PG)
            cur.execute('UPDATE news SET "show" = TRUE WHERE "show" IS NULL;')
            print(f"Column 'show' added successfully to {name}.")
        else:
            print(f"Column 'show' already exists in 'news' table in {name}.")

        cur.close()
        conn.close()
        print(f"[✓] {name} migration complete.")

    except Exception as e:
        print(f"[!] ERROR migrating {name}: {e}")

if __name__ == "__main__":
    # Migrate Local
    run_migration(LOCAL_URL, "Local")
    
    # Migrate Remote
    run_migration(REMOTE_URL, "Remote")
