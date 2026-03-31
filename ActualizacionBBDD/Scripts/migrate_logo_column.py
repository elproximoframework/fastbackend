import psycopg2

# Connection URLs
LOCAL_URL = "postgresql://space_user:space_password@localhost:5433/space_db"
REMOTE_URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"

def add_logo_column(url, name):
    print(f"\n--- Adding logo column to {name} ---")
    try:
        conn = psycopg2.connect(url)
        conn.autocommit = True
        cur = conn.cursor()
        
        # Check if column exists
        cur.execute("""
            SELECT count(*) FROM information_schema.columns 
            WHERE table_name='companies' AND column_name='logo'
        """)
        exists = cur.fetchone()[0] > 0
        
        if not exists:
            print(f"Adding 'logo' column to companies table in {name}...")
            cur.execute("ALTER TABLE companies ADD COLUMN logo VARCHAR;")
            print(f"[✓] 'logo' column added to {name}.")
        else:
            print(f"[!] 'logo' column already exists in {name}.")
            
        cur.close()
        conn.close()
    except Exception as e:
        print(f"[!] ERROR in {name}: {e}")

if __name__ == "__main__":
    add_logo_column(LOCAL_URL, "Local")
    add_logo_column(REMOTE_URL, "Remote")
