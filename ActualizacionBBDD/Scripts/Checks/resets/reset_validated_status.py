import psycopg2
import sys

# Database URLs
LOCAL_URL = "postgresql://space_user:space_password@localhost:5433/space_db"
REMOTE_URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"

def reset_validated_status(url, name):
    try:
        conn = psycopg2.connect(url)
        cur = conn.cursor()
        print(f"--- Resetting 'validated' status in {name} ---")
        
        # Resetting both validation flags to ensure a clean state
        # given the recent implementation of dual validation.
        cur.execute("""
            UPDATE companies 
            SET validated = FALSE, 
                company_validated = FALSE;
        """)
        
        conn.commit()
        count = cur.rowcount
        print(f"Successfully reset validation for {count} records in {name}")
        
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error resetting {name}: {e}", file=sys.stderr)

if __name__ == "__main__":
    print("WARNING: This script will set 'validated' and 'company_validated' to FALSE for ALL records.")
    print("Databases: LOCAL and REMOTE")
    
    reset_validated_status(LOCAL_URL, "LOCAL")
    reset_validated_status(REMOTE_URL, "REMOTE")
