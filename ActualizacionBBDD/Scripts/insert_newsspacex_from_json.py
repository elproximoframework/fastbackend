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

def upsert_news_item(cur, item):
    """
    Upserts a news item into the newsspacex table.
    Uses 'slug' as the unique identifier.
    """
    slug = item.get("slug")
    if not slug:
        print("[!] Skipping record: 'slug' field is missing.")
        return

    # Filter out keys that shouldn't be in the UPDATE/INSERT
    # Exclude 'id' as it's auto-increment.
    data = {k: v for k, v in item.items() if k != 'id'}
    
    # JSONB columns (dict/list) must be wrapped with Json() for psycopg2
    JSON_COLUMNS = {'tags', 'tags_en'}
    cols = list(data.keys())
    vals = [
        Json(data[k]) if k in JSON_COLUMNS and isinstance(data[k], (dict, list)) else data[k]
        for k in cols
    ]

    try:
        # Check if item exists by slug
        cur.execute("SELECT id FROM newsspacex WHERE slug = %s", (slug,))
        exists = cur.fetchone()

        if exists:
            # UPDATE: Quote identifiers for safety
            set_clauses = [sql.SQL("{} = %s").format(sql.Identifier(k)) for k in cols]
            query = sql.SQL("UPDATE newsspacex SET {} WHERE slug = %s").format(
                sql.SQL(', ').join(set_clauses)
            )
            cur.execute(query, vals + [slug])
            print(f"[✓] Updated: {slug}")
        else:
            # INSERT
            query = sql.SQL("INSERT INTO newsspacex ({}) VALUES ({})").format(
                sql.SQL(', ').join(map(sql.Identifier, cols)),
                sql.SQL(', ').join([sql.Placeholder()] * len(vals))
            )
            cur.execute(query, vals)
            print(f"[✓] Inserted: {slug}")
            
    except Exception as e:
        print(f"[!] Error processing {slug}: {e}")
        raise e

def process_file(file_path):
    if not os.path.exists(file_path):
        print(f"[!] File not found: {file_path}")
        return

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # Support both single object and list of objects
        items = data if isinstance(data, list) else [data]

        for label, url in [("Local", LOCAL_URL), ("Remote", REMOTE_URL)]:
            print(f"\n--- Processing {label} ---")
            try:
                conn = psycopg2.connect(url)
                conn.autocommit = False 
                cur = conn.cursor()
                for item in items:
                    upsert_news_item(cur, item)
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
    parser = argparse.ArgumentParser(description="Upsert SpaceX news items from JSON into Local and Remote databases.")
    parser.add_argument("file", help="Path to the JSON file.")
    args = parser.parse_args()
    
    process_file(args.file)
