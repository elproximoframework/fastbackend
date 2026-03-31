import psycopg2

LOCAL_URL = "postgresql://space_user:space_password@localhost:5433/space_db"
REMOTE_URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"

def diagnostic(url, label):
    print(f"\n--- Diagnostic for {label} ---")
    try:
        conn = psycopg2.connect(url)
        cur = conn.cursor()
        
        # List tables
        cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
        tables = [r[0] for r in cur.fetchall()]
        print(f"Tables: {tables}")
        
        if 'companies' in tables:
            # List columns
            cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'companies'")
            cols = [r[0] for r in cur.fetchall()]
            print(f"Columns in 'companies': {cols}")
            
            # Try a simple insert
            try:
                cur.execute("INSERT INTO companies (name) VALUES (%s) RETURNING id", ("DIAGNOSTIC_TEST",))
                new_id = cur.fetchone()[0]
                print(f"Successfully inserted test row into 'companies', ID: {new_id}")
                # Clean up
                cur.execute("DELETE FROM companies WHERE id = %s", (new_id,))
                conn.commit()
            except Exception as e:
                print(f"Insert test failed: {e}")
                conn.rollback()
        else:
            print("Table 'companies' NOT FOUND!")
            
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    diagnostic(LOCAL_URL, "Local")
    diagnostic(REMOTE_URL, "Remote")
