import psycopg2

LOCAL_URL = "postgresql://space_user:space_password@localhost:5433/space_db"
REMOTE_URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"

def check_all_slugs():
    slugs = ['momentus', 'moog-space', 'morpheus-space', 'motiv-space-systems', 'mpower-technology', 'muon-space', 'mynaric', 'myriota', 'nanoracks', 'nasa-ames']
    for label, url in [("Local", LOCAL_URL), ("Remote", REMOTE_URL)]:
        print(f"\n--- Checking {label} ---")
        try:
            conn = psycopg2.connect(url)
            cur = conn.cursor()
            cur.execute("SELECT id, name, slug FROM companies WHERE slug = ANY(%s)", (slugs,))
            rows = cur.fetchall()
            if not rows:
                print("No conflicts found.")
            for row in rows:
                print(f"ID: {row[0]}, Name: {row[1]}, Slug: {row[2]}")
            cur.close()
            conn.close()
        except Exception as e:
            print(f"Error checking {label}: {e}")

if __name__ == "__main__":
    check_all_slugs()
