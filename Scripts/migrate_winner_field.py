import sqlite3
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

# We need to know which DB we are using. .env likely has DATABASE_URL
db_url = os.getenv("DATABASE_URL", "sqlite:///./database.db")

if db_url.startswith("sqlite"):
    db_path = db_url.replace("sqlite:///", "")
    print(f"Updating SQLite database at {db_path}...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute("ALTER TABLE challenges ADD COLUMN actual_event_date DATETIME")
        print("Column actual_event_date added successfully.")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("Column already exists.")
        else:
            print(f"Error: {e}")
    conn.commit()
    conn.close()
else:
    # For PostgreSQL (assuming it might be used based on local docs)
    print("PostgreSQL detected or unknown DB. Please run migration manually or ensure column exists.")
    # In a real environment I would use alembic, but I'll try to use SQLAlchemy to check/add
    from sqlalchemy import create_engine, text
    engine = create_engine(db_url)
    with engine.connect() as conn:
        try:
            conn.execute(text("ALTER TABLE challenges ADD COLUMN IF NOT EXISTS actual_event_date TIMESTAMP WITH TIME ZONE"))
            conn.commit()
            print("Column checked/added successfully to PG.")
        except Exception as e:
            print(f"Error adding column to PG: {e}")
