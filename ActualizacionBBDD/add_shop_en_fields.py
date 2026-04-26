import os
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Add parent directory to path to find .env if needed
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'))

LOCAL_DB_URL = os.getenv("DATABASE_URL")
REMOTE_DB_URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"

def add_columns(db_url, label):
    if not db_url:
        print(f"[{label}] Skip: URL not provided")
        return
        
    print(f"[{label}] Connecting to {db_url}...")
    try:
        engine = create_engine(db_url)
        with engine.connect() as conn:
            # Add name_en
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='shop_products' AND column_name='name_en';
            """))
            if result.fetchone():
                print(f"[{label}] Column 'name_en' already exists.")
            else:
                print(f"[{label}] Adding column 'name_en'...")
                conn.execute(text("ALTER TABLE shop_products ADD COLUMN name_en VARCHAR;"))
                conn.commit()
                print(f"[{label}] Column 'name_en' added.")

            # Add description_en
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='shop_products' AND column_name='description_en';
            """))
            if result.fetchone():
                print(f"[{label}] Column 'description_en' already exists.")
            else:
                print(f"[{label}] Adding column 'description_en'...")
                conn.execute(text("ALTER TABLE shop_products ADD COLUMN description_en VARCHAR;"))
                conn.commit()
                print(f"[{label}] Column 'description_en' added.")
                
    except Exception as e:
        print(f"[{label}] Error: {e}")

if __name__ == "__main__":
    print("Starting migration for shop_products table...")
    add_columns(LOCAL_DB_URL, "LOCAL")
    add_columns(REMOTE_DB_URL, "REMOTE")
    print("Migration finished.")
