import psycopg2

# Connection URLs
LOCAL_URL = "postgresql://space_user:space_password@localhost:5433/space_db"
REMOTE_URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"

def update_aac_logo(url, name):
    print(f"\n--- Updating AAC Clyde Space logo in {name} ---")
    try:
        conn = psycopg2.connect(url)
        conn.autocommit = True
        cur = conn.cursor()
        
        cur.execute("UPDATE companies SET logo = %s WHERE name = %s", ("aac-clyde-space.png", "AAC Clyde Space"))
        print(f"[✓] AAC Clyde Space logo updated in {name}.")
            
        cur.close()
        conn.close()
    except Exception as e:
        print(f"[!] ERROR in {name}: {e}")

if __name__ == "__main__":
    update_aac_logo(LOCAL_URL, "Local")
    update_aac_logo(REMOTE_URL, "Remote")
