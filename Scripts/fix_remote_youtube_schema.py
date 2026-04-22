import psycopg2

REMOTE_URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"

def fix_schema():
    try:
        conn = psycopg2.connect(REMOTE_URL)
        conn.autocommit = True
        cur = conn.cursor()
        
        print("Checking remote schema for 'youtube' table...")
        
        # Add 'own' column if it doesn't exist
        cur.execute("ALTER TABLE youtube ADD COLUMN IF NOT EXISTS own BOOLEAN DEFAULT FALSE")
        # Add 'show' column if it doesn't exist
        cur.execute("ALTER TABLE youtube ADD COLUMN IF NOT EXISTS show BOOLEAN DEFAULT TRUE")
        # Add 'description_en' if missing
        cur.execute("ALTER TABLE youtube ADD COLUMN IF NOT EXISTS description_en TEXT")
        
        # Check if 'url' has a unique constraint for UPSERT support
        try:
            cur.execute("ALTER TABLE youtube ADD CONSTRAINT unique_youtube_url UNIQUE (url)")
            print("Added unique constraint on 'url'.")
        except Exception:
            print("Unique constraint on 'url' already exists or could not be added.")
            
        print("Schema update completed on Remote DB.")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error updating remote schema: {e}")

if __name__ == "__main__":
    fix_schema()
