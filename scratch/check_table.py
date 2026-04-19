import os
import sys
from sqlalchemy import inspect
from dotenv import load_dotenv

# Add current directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import engine

def check_table_exists():
    print(f"Checking database: {engine.url}")
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    table_name = "media_sources"
    if table_name in tables:
        print(f"SUCCESS: Table '{table_name}' exists.")
        # Check columns
        columns = [c['name'] for c in inspector.get_columns(table_name)]
        print(f"Columns: {', '.join(columns)}")
    else:
        print(f"ERROR: Table '{table_name}' NOT found.")
        print(f"Available tables: {', '.join(tables)}")

if __name__ == "__main__":
    check_table_exists()
