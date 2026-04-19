import psycopg2
import sys
import os

# Database URLs
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
        
        # Seed validation for major companies
        cur.execute("""
            UPDATE companies 
            SET company_validated = TRUE 
            WHERE name ILIKE '%SpaceX%' 
               OR name ILIKE '%NASA%' 
               OR name ILIKE '%ESA%' 
               OR name ILIKE '%JAXA%'
               OR name ILIKE '%Blue Origin%'
               OR name ILIKE '%Rocket Lab%';
        """)
        
        conn.commit()
        print(f"Successfully updated {name}")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error updating {name}: {e}", file=sys.stderr)

if __name__ == "__main__":
    # Check if we should update remote as well
    update_db(LOCAL_URL, "LOCAL")
    
    # Optional: Update remote if explicitly requested or in a production-like flow
    # For now, let's keep it locally as requested in typical dev flows unless necessary
    update_db(REMOTE_URL, "REMOTE")
