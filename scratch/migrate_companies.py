import psycopg2

LOCAL_URL = "postgresql://space_user:space_password@localhost:5433/space_db"
REMOTE_URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"

def run_migration(url_str, name):
    print(f"Migrating {name}...")
    try:
        conn = psycopg2.connect(url_str)
        conn.autocommit = True
        cur = conn.cursor()
        
        # Check if column exists first to avoid error if already runs
        cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'companies' AND column_name = 'validated'")
        if cur.fetchone():
            print(f"Column 'validated' already exists in {name}.")
        else:
            cur.execute("ALTER TABLE companies ADD COLUMN validated BOOLEAN DEFAULT FALSE;")
            print(f"Successfully added 'validated' column to {name}.")
            
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error migrating {name}: {e}")

if __name__ == "__main__":
    run_migration(LOCAL_URL, "LOCAL")
    run_migration(REMOTE_URL, "REMOTE")
