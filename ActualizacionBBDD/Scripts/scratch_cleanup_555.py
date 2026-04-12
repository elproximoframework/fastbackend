import psycopg2

LOCAL_URL = "postgresql://space_user:space_password@localhost:5433/space_db"
REMOTE_URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"

def cleanup_duplicates():
    for label, url in [("Local", LOCAL_URL), ("Remote", REMOTE_URL)]:
        print(f"--- Cleaning {label} ---")
        try:
            conn = psycopg2.connect(url)
            cur = conn.cursor()
            
            # Delete the newly created record that used the wrong name
            cur.execute("DELETE FROM companies WHERE name = 'Advanced Navigation' AND id > 560")
            print(f"Deleted duplicate record in {label}")
            
            # Rename the original record 555 so it matches the JSON's name
            cur.execute("UPDATE companies SET name = 'Advanced Navigation' WHERE id = 555")
            print(f"Renamed record 555 to 'Advanced Navigation' in {label}")
            
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            print(f"Error in {label}: {e}")

if __name__ == "__main__":
    cleanup_duplicates()
