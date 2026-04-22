import psycopg2

LOCAL_URL = "postgresql://space_user:space_password@localhost:5433/space_db"

def fix_local_schema():
    try:
        conn = psycopg2.connect(LOCAL_URL)
        conn.autocommit = True
        cur = conn.cursor()
        
        print("Checking local schema for 'youtube' table...")
        
        # Add constraint for UPSERT
        try:
            cur.execute("ALTER TABLE youtube ADD CONSTRAINT unique_youtube_url_local UNIQUE (url)")
            print("Added unique constraint on 'url' (Local).")
        except Exception:
            print("Unique constraint on 'url' already exists or could not be added (Local).")
            
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error updating local schema: {e}")

if __name__ == "__main__":
    fix_local_schema()
