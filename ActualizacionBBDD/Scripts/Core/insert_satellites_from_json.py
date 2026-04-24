import os
import json
import psycopg2
from psycopg2 import sql
from psycopg2.extras import Json
import sys
import argparse

# Database URLs
LOCAL_URL = "postgresql://space_user:space_password@localhost:5433/space_db"
REMOTE_URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"

def upsert_satellite(cur, satellite):
    """
    Upserts a satellite record into the database.
    Handles CamelCase column names correctly using psycopg2.sql to quote identifiers.
    """
    name = satellite.get("name")
    if not name:
        print("[!] Skipping record: 'name' field is missing.")
        return

    # In this version, we take the JSON keys directly and treat them as column names.
    # Exclude 'name' and 'id' from the data dict for the SET/COLUMNS clauses.
    data = {k: v for k, v in satellite.items() if k != 'name' and k != 'id'}
    
    # Automatic JSON serialization for known list/dict fields (if any)
    json_candidates = []
    for field in json_candidates:
        if field in data and (isinstance(data[field], (dict, list))):
            data[field] = Json(data[field])

    cols = list(data.keys())
    vals = [data[k] for k in cols]

    try:
        # Check if satellite exists
        cur.execute("SELECT id FROM satellites WHERE name = %s", (name,))
        exists = cur.fetchone()

        if exists:
            # UPDATE
            set_clauses = [sql.SQL("{} = %s").format(sql.Identifier(k)) for k in cols]
            query = sql.SQL("UPDATE satellites SET {} WHERE name = %s").format(
                sql.SQL(', ').join(set_clauses)
            )
            cur.execute(query, vals + [name])
            print(f"[OK] Updated: {name}")
        else:
            # INSERT
            query = sql.SQL("INSERT INTO satellites ({}, name) VALUES ({}, %s)").format(
                sql.SQL(', ').join(map(sql.Identifier, cols)),
                sql.SQL(', ').join([sql.Placeholder()] * len(vals))
            )
            cur.execute(query, vals + [name])
            print(f"[OK] Inserted: {name}")
            
    except Exception as e:
        print(f"[!] Error processing {name}: {e}")
        raise e

def process_file(file_path):
    if not os.path.exists(file_path):
        print(f"[!] File not found: {file_path}")
        return

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # Support both single object and list of objects
        satellites = data if isinstance(data, list) else [data]

        for label, url in [("Local", LOCAL_URL), ("Remote", REMOTE_URL)]:
            print(f"\n--- Processing {label} ---")
            try:
                conn = psycopg2.connect(url)
                conn.autocommit = False 
                cur = conn.cursor()
                for satellite in satellites:
                    upsert_satellite(cur, satellite)
                conn.commit()
                cur.close()
                conn.close()
                print(f"[OK] {label} sync completed successfully.")
            except Exception as e:
                print(f"[!] ERROR in {label}: {e}")
                
    except json.JSONDecodeError:
        print(f"[!] Invalid JSON format in {file_path}")
    except Exception as e:
        print(f"[!] Unexpected error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upsert satellites from JSON into Local and Remote databases.")
    parser.add_argument("file", help="Path to the JSON file.")
    args = parser.parse_args()
    
    process_file(args.file)
