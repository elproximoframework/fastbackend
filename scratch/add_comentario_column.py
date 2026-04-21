import sqlalchemy
from sqlalchemy import create_engine, text
import sys

LOCAL_URL = "postgresql://space_user:space_password@localhost:5433/space_db"
REMOTE_URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"

def add_column(url, name):
    print(f"Connecting to {name}...")
    try:
        engine = create_engine(url)
        with engine.connect() as conn:
            # Check if column exists first to avoid errors on re-run
            check_query = text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='companies' AND column_name='comentario';
            """)
            result = conn.execute(check_query).fetchone()
            
            if not result:
                print(f"Adding 'comentario' column to 'companies' table in {name}...")
                conn.execute(text("ALTER TABLE companies ADD COLUMN comentario TEXT;"))
                conn.commit()
                print("Column added successfully.")
            else:
                print(f"Column 'comentario' already exists in {name}.")
                
            # Verify
            result = conn.execute(check_query).fetchone()
            if result:
                print(f"Verification successful: 'comentario' found in {name}.")
            else:
                print(f"Verification failed: 'comentario' NOT found in {name}.")
                
    except Exception as e:
        print(f"Error connecting to {name}: {e}")

if __name__ == "__main__":
    add_column(LOCAL_URL, "LOCAL")
    print("-" * 20)
    add_column(REMOTE_URL, "REMOTE")
