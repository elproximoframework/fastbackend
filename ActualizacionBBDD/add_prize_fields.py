import os
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    print("Error: DATABASE_URL not found")
    sys.exit(1)

engine = create_engine(DATABASE_URL)

def run_migration():
    with engine.connect() as conn:
        columns = [
            ("prize_description", "TEXT"),
            ("prize_description_en", "TEXT"),
            ("prize_image_url", "TEXT")
        ]
        
        for col_name, col_type in columns:
            print(f"Checking if column '{col_name}' exists...")
            result = conn.execute(text(f"""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='challenges' AND column_name='{col_name}';
            """))
            
            if result.fetchone():
                print(f"Column '{col_name}' already exists.")
            else:
                print(f"Adding column '{col_name}' to 'challenges' table...")
                conn.execute(text(f"ALTER TABLE challenges ADD COLUMN {col_name} {col_type};"))
                conn.commit()
                print(f"Column '{col_name}' added successfully.")

if __name__ == "__main__":
    run_migration()
