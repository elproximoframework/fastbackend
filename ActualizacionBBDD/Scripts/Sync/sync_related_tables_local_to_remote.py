import sys
import os
from sqlalchemy import create_engine, text, MetaData, Table

# Database URLs
LOCAL_URL = "postgresql://space_user:space_password@localhost:5433/space_db"
REMOTE_URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"

def restore_related_tables():
    print("Starting restoration of related tables (rockets, satellites, launches)...")
    
    local_engine = create_engine(LOCAL_URL)
    remote_engine = create_engine(REMOTE_URL)
    
    tables_to_sync = ['rockets', 'satellites', 'launches']
    
    try:
        for table_name in tables_to_sync:
            print(f"\n--- Syncing table: {table_name} ---")
            
            # 1. Reflect local schema
            local_metadata = MetaData()
            table = Table(table_name, local_metadata, autoload_with=local_engine)
            
            # 2. Fetch data from local
            print(f"Fetching data from local '{table_name}'...")
            with local_engine.connect() as conn:
                result = conn.execute(table.select())
                rows = [dict(row._mapping) for row in result]
            print(f"Fetched {len(rows)} records from local.")
            
            if not rows:
                print(f"No records found in local '{table_name}'. Skipping.")
                continue

            # 3. Clear remote table (just in case, though they should be empty)
            print(f"Clearing remote '{table_name}'...")
            with remote_engine.connect() as conn:
                # We use RESTART IDENTITY but NOT CASCADE here since we only want to clear this table
                conn.execute(text(f"TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE;"))
                conn.commit()
            print(f"Remote '{table_name}' cleared.")
            
            # 4. Insert into remote
            print(f"Inserting {len(rows)} records into remote '{table_name}'...")
            remote_metadata = MetaData()
            remote_table = Table(table_name, remote_metadata, autoload_with=remote_engine)
            
            with remote_engine.connect() as conn:
                conn.execute(remote_table.insert(), rows)
                conn.commit()
            print(f"Insertion into '{table_name}' complete.")
            
            # 5. Update sequence
            with remote_engine.connect() as conn:
                max_id = conn.execute(text(f"SELECT MAX(id) FROM {table_name}")).scalar()
                if max_id:
                    seq_name = f"{table_name}_id_seq"
                    conn.execute(text(f"SELECT setval('{seq_name}', {max_id}, true)"))
                    conn.commit()
                    print(f"Sequence '{seq_name}' updated to {max_id}.")
        
        print("\nSUCCESS: Restoration finished successfully.")
        
    except Exception as e:
        print(f"\nERROR during restoration: {e}")
        sys.exit(1)

if __name__ == "__main__":
    restore_related_tables()
