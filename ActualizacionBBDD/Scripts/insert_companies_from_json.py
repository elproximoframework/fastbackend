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

def upsert_company(cur, company):
    """
    Upserts a company record into the database.
    Handles CamelCase column names correctly using psycopg2.sql to quote identifiers.
    """
    name = company.get("name")
    if not name:
        print("[!] Skipping record: 'name' field is missing.")
        return

    # In this version, we take the JSON keys directly and treat them as column names.
    # This allows the script to be flexible as long as the JSON matches the DB schema.
    # We exclude 'name' from the data dict because it's used in the WHERE clause.
    data = {k: v for k, v in company.items() if k != 'name' and k != 'id'}
    
    # Automatic JSON serialization for known list/dict fields
    # Based on the schema: coordinates, tags, socialLinks, keyPrograms
    json_candidates = ['coordinates', 'tags', 'socialLinks', 'keyPrograms']
    for field in json_candidates:
        if field in data and (isinstance(data[field], (dict, list))):
            data[field] = Json(data[field])

    cols = list(data.keys())
    vals = [data[k] for k in cols]

    try:
        # Check if company exists
        cur.execute("SELECT id FROM companies WHERE name = %s", (name,))
        exists = cur.fetchone()

        if exists:
            # UPDATE: Use sql.Identifier to ensure column names (like "countryName") are quoted.
            set_clauses = [sql.SQL("{} = %s").format(sql.Identifier(k)) for k in cols]
            query = sql.SQL("UPDATE companies SET {} WHERE name = %s").format(
                sql.SQL(', ').join(set_clauses)
            )
            cur.execute(query, vals + [name])
            print(f"[✓] Updated: {name}")
        else:
            # INSERT: Use sql.Identifier for column names.
            query = sql.SQL("INSERT INTO companies ({}, name) VALUES ({}, %s)").format(
                sql.SQL(', ').join(map(sql.Identifier, cols)),
                sql.SQL(', ').join([sql.Placeholder()] * len(vals))
            )
            cur.execute(query, vals + [name])
            print(f"[✓] Inserted: {name}")
            
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
        companies = data if isinstance(data, list) else [data]

        for label, url in [("Local", LOCAL_URL), ("Remote", REMOTE_URL)]:
            print(f"\n--- Processing {label} ---")
            try:
                conn = psycopg2.connect(url)
                # Use autocommit or manual commit
                conn.autocommit = False 
                cur = conn.cursor()
                for company in companies:
                    upsert_company(cur, company)
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
    parser = argparse.ArgumentParser(description="Upsert companies from JSON into Local and Remote databases.")
    parser.add_argument("file", help="Path to the JSON file.")
    args = parser.parse_args()
    
    process_file(args.file)
