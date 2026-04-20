import psycopg2
import sys

# Database URLs
LOCAL_URL = "postgresql://space_user:space_password@localhost:5433/space_db"
REMOTE_URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"

def link_launches(db_url, label):
    print(f"\n--- Processing {label} ---")
    try:
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()

        # 1. Fetch all rockets for matching
        cur.execute("SELECT id, name, manufacturer_id FROM rockets")
        rockets = cur.fetchall()
        rocket_map = {r[1].lower(): (r[0], r[2]) for r in rockets}

        # 2. Fetch launches with NULL rocket_id
        cur.execute("SELECT id, name FROM launches WHERE rocket_id IS NULL")
        launches = cur.fetchall()
        print(f"Found {len(launches)} launches with NULL rocket_id.")

        links_count = 0
        for l_id, l_name in launches:
            # Try matching logic
            match_name = l_name.split('|')[0].strip().lower()
            
            if match_name in rocket_map:
                r_id, m_id = rocket_map[match_name]
                
                # Update launch
                # We update rocket_id and ALSO provider_id if it's NULL
                cur.execute("""
                    UPDATE launches 
                    SET rocket_id = %s, 
                        provider_id = COALESCE(provider_id, %s)
                    WHERE id = %s
                """, (r_id, m_id, l_id))
                links_count += 1
                # print(f"Linked: '{l_name}' -> RocketID: {r_id}")

        conn.commit()
        print(f"Successfully linked {links_count} launches in {label}.")
        
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error in {label}: {e}")

if __name__ == "__main__":
    link_launches(LOCAL_URL, "Local")
    link_launches(REMOTE_URL, "Remote")
