import sys
import os
from sqlalchemy import create_engine, text, MetaData, Table

# Database URLs
LOCAL_URL = "postgresql://space_user:space_password@localhost:5433/space_db"
REMOTE_URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"

def sync_companies():
    print("Starting synchronization of 'companies' table...")
    
    local_engine = create_engine(LOCAL_URL)
    remote_engine = create_engine(REMOTE_URL)
    
    metadata = MetaData()
    print("Reflecting local schema...")
    companies_table = Table('companies', metadata, autoload_with=local_engine)
    
    try:
        # 1. Fetch data from local
        print("Fetching data from local database...")
        with local_engine.connect() as conn:
            result = conn.execute(companies_table.select())
            rows = [dict(row._mapping) for row in result]
        print(f"Fetched {len(rows)} records from local.")
        
        if not rows:
            print("No records found in local database. Aborting.")
            return

        # 2. Clear remote table
        print("Clearing remote 'companies' table (CASCADE)...")
        with remote_engine.connect() as conn:
            # Note: CASCADE will also clear rockets, satellites, and launches on remote.
            conn.execute(text("TRUNCATE TABLE companies RESTART IDENTITY CASCADE;"))
            conn.commit()
        print("Remote table cleared.")
        
        # 3. Insert into remote
        print(f"Inserting {len(rows)} records into remote database...")
        # We need to recreate the table object for the remote engine to ensure compatibility
        remote_metadata = MetaData()
        remote_companies_table = Table('companies', remote_metadata, autoload_with=remote_engine)
        
        with remote_engine.connect() as conn:
            # Batch insertion
            conn.execute(remote_companies_table.insert(), rows)
            conn.commit()
        print("Insertion complete.")
        
        # 4. Update sequence
        with remote_engine.connect() as conn:
            max_id = conn.execute(text("SELECT MAX(id) FROM companies")).scalar()
            if max_id:
                # PostgreSQL specific sequence update
                conn.execute(text(f"SELECT setval('companies_id_seq', {max_id}, true)"))
                conn.commit()
                print(f"Sequence 'companies_id_seq' updated to {max_id}.")
        
        print("\nSUCCESS: Synchronization finished successfully.")
        print(f"Remote 'companies' table now has {len(rows)} records.")
        print("Warning: Related tables (rockets, satellites, launches) on remote were emptied by CASCADE.")
        
    except Exception as e:
        print(f"\nERROR during synchronization: {e}")
        sys.exit(1)

if __name__ == "__main__":
    sync_companies()
