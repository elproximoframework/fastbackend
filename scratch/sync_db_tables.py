import os
import sys
from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base

# Add current directory to path
sys.path.append(os.getcwd())
from app.models import Base

LOCAL_DB = "postgresql://space_user:space_password@localhost:5433/space_db"
RAILWAY_DB = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"

def check_and_create(db_url, label):
    print(f"\n--- Checking {label} Database ---")
    try:
        engine = create_engine(db_url)
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        table_name = "media_sources"
        if table_name in tables:
            print(f"SUCCESS: Table '{table_name}' already exists in {label}.")
        else:
            print(f"INFO: Table '{table_name}' not found in {label}. Creating it now...")
            Base.metadata.create_all(bind=engine, tables=[Base.metadata.tables[table_name]])
            # Confirm creation
            inspector = inspect(engine)
            if table_name in inspector.get_table_names():
                print(f"SUCCESS: Table '{table_name}' created successfully in {label}.")
            else:
                print(f"ERROR: Failed to create table '{table_name}' in {label}.")
        
        # Check columns anyway to be sure
        if table_name in inspector.get_table_names():
            columns = [c['name'] for c in inspector.get_columns(table_name)]
            print(f"Columns found: {len(columns)}")
            
    except Exception as e:
        print(f"ERROR checking {label}: {e}")

if __name__ == "__main__":
    check_and_create(LOCAL_DB, "LOCAL")
    check_and_create(RAILWAY_DB, "RAILWAY")
