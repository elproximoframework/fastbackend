import psycopg2

URL = "postgresql://space_user:space_password@localhost:5433/space_db"

def check_db():
    try:
        conn = psycopg2.connect(URL)
        cur = conn.cursor()
        
        # Check connection
        print("✅ SUCCESS: Connected to PostgreSQL on port 5433")
        
        # Check tables
        cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
        tables = cur.fetchall()
        print(f"Total tables found: {len(tables)}")
        for table in tables:
            print(f"  - {table[0]}")
            
        # Check Satellites specifically
        print("\nChecking 'satellites' table...")
        cur.execute("SELECT COUNT(*) FROM satellites")
        count = cur.fetchone()[0]
        print(f"Total satellites in DB: {count}")
        
        # Check for the new column
        cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name='satellites' AND column_name='description_en'")
        column = cur.fetchone()
        if column:
            print("✅ 'description_en' column exists.")
            
            # Sample data
            cur.execute("SELECT name, description_en FROM satellites LIMIT 2")
            rows = cur.fetchall()
            for row in rows:
                print(f"  - Satellite: {row[0]}")
                print(f"    EN Desc: {row[1][:70]}...")
        else:
            print("❌ 'description_en' column NOT FOUND.")
            
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ FAILURE: {e}")

if __name__ == "__main__":
    check_db()
