import psycopg2

def verify_data(url, label):
    print(f"\n--- Verifying {label} ---")
    try:
        conn = psycopg2.connect(url)
        cur = conn.cursor()
        names = [
            "Pale Blue", 
            "Tenchijin", 
            "ArkEdge Space", 
            "Kawasaki Heavy Industries (Space Division)", 
            "NEC Space Technologies", 
            "Space One", 
            "China National Space Administration (CNSA)", 
            "CASC (China Aerospace Science and Technology Corp.)", 
            "CASIC (China Aerospace Science and Industry Corp.)", 
            "iSpace (Beijing Interstellar Glory)"
        ]
        placeholders = ', '.join(['%s'] * len(names))
        query = f"SELECT id, name, slug, country, city FROM companies WHERE name IN ({placeholders}) ORDER BY id"
        cur.execute(query, names)
        rows = cur.fetchall()
        for row in rows:
            print(f"ID: {row[0]} | Name: {row[1]} | Slug: {row[2]} | Country: {row[3]} | City: {row[4]}")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    LOCAL_URL = "postgresql://space_user:space_password@localhost:5433/space_db"
    REMOTE_URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"
    verify_data(LOCAL_URL, "Local")
    verify_data(REMOTE_URL, "Remote")
