import sys
import os

# Add the parent directory to sys.path to allow importing from 'app'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from app.models import Base
import sqlalchemy

LOCAL_DB_URL = "postgresql://space_user:space_password@localhost:5433/space_db"
REMOTE_DB_URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"

def create_tables(db_url, name):
    print(f"--- Creating tables in {name} ---")
    try:
        engine = create_engine(db_url)
        # Check connection
        with engine.connect() as conn:
            print(f"Connected to {name}")
        
        # Create tables
        Base.metadata.create_all(bind=engine)
        print(f"Tables created/verified in {name}")
    except Exception as e:
        print(f"Error creating tables in {name}: {str(e)}")

if __name__ == "__main__":
    create_tables(LOCAL_DB_URL, "LOCAL")
    print("\n")
    create_tables(REMOTE_DB_URL, "REMOTE")
