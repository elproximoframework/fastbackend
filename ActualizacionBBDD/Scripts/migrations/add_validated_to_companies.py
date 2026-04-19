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
                               WHERE table_name='companies' AND column_name='validated') THEN
                    ALTER TABLE companies ADD COLUMN validated BOOLEAN DEFAULT FALSE;
                END IF;
            END $$;
        """)
        print(f"Column 'validated' ensured in {name}")
        
        # Mark some companies as validated
        v_list = ['SpaceX', 'NASA', 'ESA', 'Blue Origin', 'Rocket Lab', 'PLD Space', 'Clyde Space', 'ArianeGroup', 'Satlantis', 'Open Cosmos']
        updated_count = 0
        for company in v_list:
            cur.execute("UPDATE companies SET validated = TRUE WHERE name ILIKE %s;", (f"%{company}%",))
            updated_count += cur.rowcount
            
        conn.commit()
        print(f"Successfully updated {updated_count} companies in {name}")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error updating {name}: {e}", file=sys.stderr)

if __name__ == "__main__":
    update_db(LOCAL_URL, "LOCAL")
    update_db(REMOTE_URL, "REMOTE")
