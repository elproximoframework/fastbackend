import psycopg2

LOCAL_URL = "postgresql://space_user:space_password@localhost:5433/space_db"
REMOTE_URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"

def diagnostic(url, label, log_file):
    log_file.write(f"\n--- Diagnostic for {label} ---\n")
    try:
        conn = psycopg2.connect(url)
        cur = conn.cursor()
        
        # List tables
        cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
        tables = [r[0] for r in cur.fetchall()]
        log_file.write(f"Tables: {tables}\n")
        
        if 'companies' in tables:
            # List columns
            cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'companies'")
            cols = [r[0] for r in cur.fetchall()]
            log_file.write(f"Columns in 'companies': {cols}\n")
            
            # Try a simple insert
            try:
                cur.execute("INSERT INTO companies (name) VALUES (%s) RETURNING id", ("DIAGNOSTIC_TEST",))
                new_id = cur.fetchone()[0]
                log_file.write(f"Successfully inserted test row into 'companies', ID: {new_id}\n")
                # Clean up
                cur.execute("DELETE FROM companies WHERE id = %s", (new_id,))
                conn.commit()
                log_file.write("Cleanup successful.\n")
            except Exception as e:
                log_file.write(f"Insert test failed: {e}\n")
                conn.rollback()
        else:
            log_file.write("Table 'companies' NOT FOUND!\n")
            
        cur.close()
        conn.close()
    except Exception as e:
        log_file.write(f"Connection failed: {e}\n")

if __name__ == "__main__":
    import os
    # Ensure it writes to the current directory of the script or the CWD
    output_path = os.path.join(os.getcwd(), "diagnostic_utf8.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        diagnostic(LOCAL_URL, "Local", f)
        diagnostic(REMOTE_URL, "Remote", f)
    print(f"Log written to {output_path}")
