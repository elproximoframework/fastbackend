import psycopg2

REMOTE_URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"

def check_qeynet():
    try:
        conn = psycopg2.connect(REMOTE_URL)
        cur = conn.cursor()
        
        # Check by name first
        cur.execute("SELECT id, name, slug FROM companies WHERE name ILIKE '%qey%net%'")
        rows = cur.fetchall()
        print("Matches by name (ILIKE '%qey%net%'):")
        for row in rows:
            print(f"ID: {row[0]}, Name: {row[1]}, Slug: {row[2]}")
            
        # Check by slug
        cur.execute("SELECT id, name, slug FROM companies WHERE slug = 'qeynet'")
        row = cur.fetchone()
        if row:
            print(f"\nMatch by slug 'qeynet':\nID: {row[0]}, Name: {row[1]}, Slug: {row[2]}")
        else:
            print("\nNo match by slug 'qeynet'")
            
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_qeynet()
