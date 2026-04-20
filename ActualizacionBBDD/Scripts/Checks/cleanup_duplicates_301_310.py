import psycopg2

LOCAL_URL = "postgresql://space_user:space_password@localhost:5433/space_db"
REMOTE_URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"

REMAPS = {
    302: 'Rocket Lab USA',
    303: 'Beyond Gravity USA',
    305: 'SAIC',
    308: 'Seraphim Space'
}

DUPLICATE_IDS = [603, 604, 605, 606]

def cleanup(url, label):
    print(f"\n--- Cleaning up {label} ---")
    try:
        conn = psycopg2.connect(url)
        cur = conn.cursor()

        # 1. Delete duplicates
        print(f"Deleting duplicates: {DUPLICATE_IDS}")
        cur.execute("DELETE FROM companies WHERE id IN %s", (tuple(DUPLICATE_IDS),))
        print(f"Deleted {cur.rowcount} rows.")

        # 2. Rename existing
        for cid, new_name in REMAPS.items():
            print(f"Renaming ID {cid} to '{new_name}'")
            cur.execute("UPDATE companies SET name = %s WHERE id = %s", (new_name, cid))
        
        conn.commit()
        cur.close()
        conn.close()
        print("[OK] Cleanup finished.")
    except Exception as e:
        print(f"[!] ERROR in {label}: {e}")

if __name__ == "__main__":
    cleanup(LOCAL_URL, "Local")
    cleanup(REMOTE_URL, "Remote")
