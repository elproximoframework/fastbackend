import psycopg2

LOCAL_URL = "postgresql://space_user:space_password@localhost:5433/space_db"
REMOTE_URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"

def validate_top_companies(url_str, name):
    print(f"Validating companies in {name}...")
    try:
        conn = psycopg2.connect(url_str)
        conn.autocommit = True
        cur = conn.cursor()
        
        # Validate SpaceX and PLD Space
        cur.execute("UPDATE companies SET validated = TRUE WHERE name ILIKE '%SpaceX%' OR name ILIKE '%PLD Space%'")
        print(f"Updated {cur.rowcount} companies in {name}.")
        
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error in {name}: {e}")

if __name__ == "__main__":
    validate_top_companies(LOCAL_URL, "LOCAL")
    validate_top_companies(REMOTE_URL, "REMOTE")
