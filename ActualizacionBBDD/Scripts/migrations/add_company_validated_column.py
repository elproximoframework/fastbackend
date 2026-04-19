import psycopg2
import sys

LOCAL_URL = "postgresql://space_user:space_password@localhost:5433/space_db"
REMOTE_URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"

def update_db(url, name):
    try:
        conn = psycopg2.connect(url)
        cur = conn.cursor()
        print(f"--- Updating {name} ---")
        
        # Add column if not exists
        cur.execute("""
            DO $$ 
            BEGIN 
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                               WHERE table_name='companies' AND column_name='company_validated') THEN
                    ALTER TABLE companies ADD COLUMN company_validated BOOLEAN DEFAULT FALSE;
                END IF;
            END $$;
        """)
        print(f"Column 'company_validated' ensured in {name}")
        
        # For testing, let's mark some as company_validated too
        # Specifically SpaceX and NASA
        cur.execute("UPDATE companies SET company_validated = TRUE WHERE name ILIKE '%SpaceX%' OR name ILIKE '%NASA%';")
        
        conn.commit()
        print(f"Successfully updated {name}")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error updating {name}: {e}", file=sys.stderr)

if __name__ == "__main__":
    update_db(LOCAL_URL, "LOCAL")
    update_db(REMOTE_URL, "REMOTE")
