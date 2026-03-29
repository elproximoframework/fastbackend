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

        # Tables to update
        tables = ["launches", "satellites"]

        for table in tables:
            # Check if 'show' column exists
            cur.execute(f"""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='{table}' AND column_name='show';
            """)
            
            if not cur.fetchone():
                print(f"Adding 'show' column to '{table}' table in {name}...")
                cur.execute(f'ALTER TABLE {table} ADD COLUMN "show" BOOLEAN DEFAULT TRUE;')
                # Update existing records to TRUE
                cur.execute(f'UPDATE {table} SET "show" = TRUE WHERE "show" IS NULL;')
                print(f"Column 'show' added successfully to '{table}' in {name}.")
            else:
                print(f"Column 'show' already exists in '{table}' table in {name}.")

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
