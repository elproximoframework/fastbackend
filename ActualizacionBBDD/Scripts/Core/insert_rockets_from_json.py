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

def upsert_rocket(cur, rocket):
    """
    Upserts a rocket record into the database.
    Handles CamelCase column names correctly using psycopg2.sql to quote identifiers.
    """
    name = rocket.get("name")
    if not name:
        print("[!] Skipping record: 'name' field is missing.")
        return

    # Exclude name and id from the data dict
    data = {k: v for k, v in rocket.items() if k != 'name' and k != 'id'}

    # Resolve manufacturer_id from manufacturer_slug if manufacturer_id is missing but slug is present
    if 'manufacturer_id' not in data and 'manufacturer_slug' in data:
        slug = data.pop('manufacturer_slug')
        cur.execute("SELECT id FROM companies WHERE slug = %s", (slug,))
        row = cur.fetchone()
        if row:
            data['manufacturer_id'] = row[0]
        else:
            print(f"[!] Warning: Company slug '{slug}' not found for rocket '{name}'.")

    cols = list(data.keys())
    vals = [data[k] for k in cols]

    try:
        # Check if rocket exists
        cur.execute("SELECT id FROM rockets WHERE name = %s", (name,))
        exists = cur.fetchone()

        if exists:
            # UPDATE: Use sql.Identifier to ensure column names (like "leoCapacity") are quoted.
            set_clauses = [sql.SQL("{} = %s").format(sql.Identifier(k)) for k in cols]
            query = sql.SQL("UPDATE rockets SET {} WHERE name = %s").format(
                sql.SQL(', ').join(set_clauses)
            )
            cur.execute(query, vals + [name])
            print(f"[OK] Updated: {name}")
        else:
            # INSERT: Use sql.Identifier for column names.
            query = sql.SQL("INSERT INTO rockets ({}, name) VALUES ({}, %s)").format(
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
        rockets = data if isinstance(data, list) else [data]

        for label, url in [("Local", LOCAL_URL), ("Remote", REMOTE_URL)]:
            print(f"\n--- Processing {label} ---")
            try:
                conn = psycopg2.connect(url)
                # Use autocommit or manual commit
                conn.autocommit = False 
                cur = conn.cursor()
                for rocket in rockets:
                    upsert_rocket(cur, rocket)
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
    parser = argparse.ArgumentParser(description="Upsert rockets from JSON into Local and Remote databases.")
    parser.add_argument("file", help="Path to the JSON file.")
    args = parser.parse_args()
    
    process_file(args.file)
