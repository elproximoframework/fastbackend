import psycopg2

LOCAL_URL = "postgresql://space_user:space_password@localhost:5433/space_db"
REMOTE_URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"

def verify_companies(url, label):
    print(f"\n--- Verifying {label} ---")
    try:
        conn = psycopg2.connect(url)
        cur = conn.cursor()
        
        companies_to_check = ["SpaceX", "Blue Origin", "PLD Space"]
        for company in companies_to_check:
            cur.execute("SELECT name, country, city, sector FROM companies WHERE name = %s", (company,))
            row = cur.fetchone()
            if row:
                print(f"[✓] {company} found: {row}")
            else:
                print(f"[X] {company} NOT FOUND")
            
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    verify_companies(LOCAL_URL, "Local")
    verify_companies(REMOTE_URL, "Remote")
