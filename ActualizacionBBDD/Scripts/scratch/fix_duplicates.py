import psycopg2

def fix_duplicates():
    urls = [
        ("Local", "postgresql://space_user:space_password@localhost:5433/space_db"),
        ("Remote", "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway")
    ]
    for label, url in urls:
        print(f"--- Fixing {label} ---")
        try:
            conn = psycopg2.connect(url)
            cur = conn.cursor()
            
            # 1. Delete the accidental insertion (ID 627 might differ on remote? No, usually IDs are incremented)
            # Actually, better to delete by name "Rocket Lab (Nueva Zelanda)" since it's the one I just inserted
            cur.execute("DELETE FROM companies WHERE name = 'Rocket Lab (Nueva Zelanda)' AND id != 565")
            print(f"Deleted duplicate insertions in {label}")
            
            # 2. Update the original ID 565 with the new name if desired
            # The prompt said IDs 561-565. Let's keep ID 565 but maybe update the name to the one in JSON?
            # Actually, I'll just stick to the original name to avoid further confusion with the upsert script
            # OR I update the original one to the new name now.
            cur.execute("UPDATE companies SET name = 'Rocket Lab (Nueva Zelanda)' WHERE id = 565")
            print(f"Renamed ID 565 in {label}")
            
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            print(f"Error in {label}: {e}")

if __name__ == "__main__":
    fix_duplicates()
