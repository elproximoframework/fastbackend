import psycopg2
from psycopg2.extras import RealDictCursor, Json
import sys

# Connection Strings
LOCAL_URL = "postgresql://space_user:space_password@localhost:5433/space_db"
REMOTE_URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"

TABLES = ["companies", "rockets", "satellites", "launches"]

def migrate_table(table_name, local_cursor, remote_cursor):
    print(f"Migrating table: {table_name}...")
    
    # 1. Get column names
    local_cursor.execute(f"SELECT * FROM {table_name} LIMIT 0")
    columns = [desc[0] for desc in local_cursor.description]
    columns_str = ", ".join([f'"{c}"' for c in columns])
    placeholders = ", ".join(["%s"] * len(columns))
    
    # 2. Fetch all data from local
    local_cursor.execute(f"SELECT * FROM {table_name}")
    rows = local_cursor.fetchall()
    
    if not rows:
        print(f"  No data found in {table_name}. Skipping.")
        return

    # 3. Clear remote table (optional but recommended for a clean sync)
    print(f"  Clearing remote {table_name}...")
    remote_cursor.execute(f"TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE;")
    
    # 4. Insert into remote
    insert_query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"
    
    for row in rows:
        # Convert row values if necessary (e.g. dict to Json for postgres)
        values = []
        for col, val in row.items():
            if isinstance(val, (dict, list)):
                values.append(Json(val))
            else:
                values.append(val)
        
        remote_cursor.execute(insert_query, tuple(values))
        
    print(f"  Successfully migrated {len(rows)} rows to {table_name}.")

def main():
    try:
        print("Connecting to Local DB...")
        local_conn = psycopg2.connect(LOCAL_URL)
        local_cur = local_conn.cursor(cursor_factory=RealDictCursor)
        
        print("Connecting to Remote DB (Railway)...")
        remote_conn = psycopg2.connect(REMOTE_URL)
        remote_conn.autocommit = True
        remote_cur = remote_conn.cursor()
        
        for table in TABLES:
            try:
                migrate_table(table, local_cur, remote_cur)
            except Exception as e:
                print(f"Error migrating {table}: {e}")
                
        print("\nMigration completed successfully!")
        
        local_cur.close()
        local_conn.close()
        remote_cur.close()
        remote_conn.close()
        
    except Exception as e:
        print(f"Critical error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
