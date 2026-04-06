import psycopg2

# Database URLs
LOCAL_URL = "postgresql://space_user:space_password@localhost:5433/space_db"
REMOTE_URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"

PREFIXES = [
    "/inventory_images/starship/",
    "/inventory_images/lanzamientos/",
    "/inventory_images/raptor/",
    "/inventory_images/super-heavy/"
]

def migrate_database(url, label):
    print(f"\n--- Migrating Inventory in {label} ---")
    try:
        conn = psycopg2.connect(url)
        cur = conn.cursor()
        
        updated_total = 0
        for prefix in PREFIXES:
            # Migrate image column
            cur.execute("SELECT id, image FROM spacex_inventory WHERE image LIKE %s", (prefix + '%',))
            rows = cur.fetchall()
            if rows:
                print(f"  Found {len(rows)} items with image prefix {prefix}")
                for item_id, old_path in rows:
                    filename = old_path.split('/')[-1]
                    cur.execute("UPDATE spacex_inventory SET image = %s WHERE id = %s", (filename, item_id))
                    updated_total += 1

            # Migrate rutainformacion column
            info_prefix = prefix.split('/')[-2] + '/'
            cur.execute("SELECT id, rutainformacion FROM spacex_inventory WHERE rutainformacion LIKE %s", (info_prefix + '%',))
            info_rows = cur.fetchall()
            if info_rows:
                print(f"  Found {len(info_rows)} items with rutainformacion prefix {info_prefix}")
                for item_id, old_path in info_rows:
                    filename = old_path.split('/')[-1]
                    cur.execute("UPDATE spacex_inventory SET rutainformacion = %s WHERE id = %s", (filename, item_id))
                    updated_total += 1
            
        conn.commit()
        cur.close()
        conn.close()
        print(f"[OK] {label}: Inventory migration completed. Updated {updated_total} items.")
    except Exception as e:
        print(f"[!] ERROR in {label}: {e}")

if __name__ == "__main__":
    migrate_database(LOCAL_URL, "Local")
    migrate_database(REMOTE_URL, "Remote")
