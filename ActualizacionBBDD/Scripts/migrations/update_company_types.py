import psycopg2

# Connection URLs
LOCAL_URL = "postgresql://space_user:space_password@localhost:5433/space_db"
REMOTE_URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"

def run_migration(url, name):
    print(f"\n--- Updating company types in {name} Database ---")
    try:
        conn = psycopg2.connect(url)
        conn.autocommit = True
        cur = conn.cursor()

        # Update mappings
        cur.execute("UPDATE companies SET type = 'corporate' WHERE type = 'contractor';")
        print(f"Updated contractor -> corporate. Rows affected: {cur.rowcount}")

        cur.execute("UPDATE companies SET type = 'academia' WHERE type = 'university';")
        print(f"Updated university -> academia. Rows affected: {cur.rowcount}")

        cur.execute("UPDATE companies SET type = 'investor' WHERE type = 'investors';")
        print(f"Updated investors -> investor. Rows affected: {cur.rowcount}")

        cur.execute("UPDATE companies SET type = 'corporate', sector = 'ground_segment' WHERE type = 'ground_segment';")
        print(f"Updated ground_segment (type) -> corporate/ground_segment. Rows affected: {cur.rowcount}")

        cur.execute("UPDATE companies SET type = 'corporate', sector = 'in_space_logistics' WHERE type = 'logistics';")
        print(f"Updated logistics (type) -> corporate/in_space_logistics. Rows affected: {cur.rowcount}")

        cur.close()
        conn.close()
        print(f"[✓] {name} migration complete.")

    except Exception as e:
        print(f"[!] ERROR migrating {name}: {e}")

if __name__ == "__main__":
    # Migrate Local
    run_migration(LOCAL_URL, "Local")
    
    # Migrate Remote
    run_migration(REMOTE_URL, "Remote")
