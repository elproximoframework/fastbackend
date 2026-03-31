import psycopg2

# Connection URLs
LOCAL_URL = "postgresql://space_user:space_password@localhost:5433/space_db"
REMOTE_URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"

def add_featured_column(url, name):
    print(f"\n--- Adding featured_espacio column to {name} ---")
    try:
        conn = psycopg2.connect(url)
        conn.autocommit = True
        cur = conn.cursor()
        
        # Check if column exists
        cur.execute("""
            SELECT count(*) FROM information_schema.columns 
            WHERE table_name='companies' AND column_name='featured_espacio'
        """)
        exists = cur.fetchone()[0] > 0
        
        if not exists:
            print(f"Adding 'featured_espacio' column to companies table in {name}...")
            cur.execute("ALTER TABLE companies ADD COLUMN featured_espacio BOOLEAN DEFAULT FALSE;")
            # Update existing to False (explicitly, though default handles it for new, but good for existing)
            cur.execute("UPDATE companies SET featured_espacio = FALSE WHERE featured_espacio IS NULL;")
            print(f"[✓] 'featured_espacio' column added to {name}.")
        else:
            print(f"[!] 'featured_espacio' column already exists in {name}.")
            
        cur.close()
        conn.close()
    except Exception as e:
        print(f"[!] ERROR in {name}: {e}")

if __name__ == "__main__":
    add_featured_column(LOCAL_URL, "Local")
    add_featured_column(REMOTE_URL, "Remote")
