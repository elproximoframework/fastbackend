import psycopg2
import sys

DATABASE_URL = "postgresql://space_user:space_password@localhost:5433/space_db"

def migrate():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        conn.autocommit = True
        cur = conn.cursor()
        
        print("Checking if 'own' column exists in 'youtube' table...")
        cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name='youtube' AND column_name='own'")
        
        if cur.fetchone():
            print("Column 'own' already exists.")
        else:
            print("Adding 'own' column to 'youtube' table...")
            cur.execute("ALTER TABLE youtube ADD COLUMN own BOOLEAN DEFAULT FALSE")
            print("Column 'own' added successfully.")

        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error during migration: {e}")
        sys.exit(1)

if __name__ == "__main__":
    migrate()
