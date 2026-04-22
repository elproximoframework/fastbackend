import os
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Add parent directory to path to find app module if needed, 
# but we can just use the DATABASE_URL directly here.
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    print("Error: DATABASE_URL not found")
    sys.exit(1)

engine = create_engine(DATABASE_URL)

def run_migration():
    with engine.connect() as conn:
        print("Checking if column 'prediction_deadline' exists...")
        result = conn.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='challenges' AND column_name='prediction_deadline';
        """))
        
        if result.fetchone():
            print("Column 'prediction_deadline' already exists.")
        else:
            print("Adding column 'prediction_deadline' to 'challenges' table...")
            conn.execute(text("ALTER TABLE challenges ADD COLUMN prediction_deadline TIMESTAMP WITH TIME ZONE;"))
            conn.commit()
            print("Column added successfully.")

if __name__ == "__main__":
    run_migration()
