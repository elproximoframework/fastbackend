import psycopg2

LOCAL_URL = "postgresql://space_user:space_password@localhost:5433/space_db"

def clean_and_fix():
    try:
        conn = psycopg2.connect(LOCAL_URL)
        conn.autocommit = True
        cur = conn.cursor()
        
        print("Cleaning duplicates...")
        cur.execute("""
            DELETE FROM youtube a USING youtube b
            WHERE a.id < b.id AND a.url = b.url;
        """)
        print(f"Removed {cur.rowcount} duplicates.")
        
        print("Adding unique constraint on 'url' (Local)...")
        cur.execute("ALTER TABLE youtube ADD CONSTRAINT unique_youtube_url UNIQUE (url)")
        print("Unique constraint added.")
        
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    clean_and_fix()
