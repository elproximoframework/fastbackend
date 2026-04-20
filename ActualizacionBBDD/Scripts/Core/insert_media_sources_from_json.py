import os
import json
import psycopg2
from psycopg2 import sql
from psycopg2.extras import Json
import sys
import argparse

# ── Database URLs ─────────────────────────────────────────────────────────────
LOCAL_URL  = "postgresql://space_user:space_password@localhost:5433/space_db"
REMOTE_URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"

# Columns stored as JSONB in PostgreSQL (must be wrapped with Json())
JSON_COLUMNS = {"content_format", "topics"}


def upsert_media_source(cur, item: dict) -> None:
    """
    Upserts a media_sources record using 'slug' as the unique key.
    - If slug exists  → UPDATE all fields.
    - If slug missing → INSERT new record.
    """
    slug = item.get("slug")
    if not slug:
        print("[!] Skipping record: 'slug' field is missing.")
        return

    # Exclude 'id' — it is autoincremental
    data = {k: v for k, v in item.items() if k != "id"}

    cols = list(data.keys())
    vals = [
        Json(data[k]) if k in JSON_COLUMNS and isinstance(data[k], (dict, list)) else data[k]
        for k in cols
    ]

    try:
        cur.execute("SELECT id FROM media_sources WHERE slug = %s", (slug,))
        exists = cur.fetchone()

        if exists:
            set_clauses = [sql.SQL("{} = %s").format(sql.Identifier(k)) for k in cols]
            query = sql.SQL("UPDATE media_sources SET {} WHERE slug = %s").format(
                sql.SQL(", ").join(set_clauses)
            )
            cur.execute(query, vals + [slug])
            print(f"  [✓] Updated : {slug}")
        else:
            query = sql.SQL("INSERT INTO media_sources ({}) VALUES ({})").format(
                sql.SQL(", ").join(map(sql.Identifier, cols)),
                sql.SQL(", ").join([sql.Placeholder()] * len(vals)),
            )
            cur.execute(query, vals)
            print(f"  [+] Inserted: {slug}")

    except Exception as exc:
        print(f"  [!] Error processing '{slug}': {exc}")
        raise


def process_file(file_path: str) -> None:
    if not os.path.exists(file_path):
        print(f"[!] File not found: {file_path}")
        return

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            raw = json.load(f)
    except json.JSONDecodeError as exc:
        print(f"[!] Invalid JSON in {file_path}: {exc}")
        return

    # Accept both a single object {} and a list of objects [{}]
    items = raw if isinstance(raw, list) else [raw]
    print(f"[i] Loaded {len(items)} record(s) from {file_path}\n")

    for label, url in [("Local", LOCAL_URL), ("Remote", REMOTE_URL)]:
        print(f"─── {label} ───────────────────────────────────────────")
        try:
            conn = psycopg2.connect(url)
            conn.autocommit = False
            cur = conn.cursor()

            for item in items:
                upsert_media_source(cur, item)

            conn.commit()
            cur.close()
            conn.close()
            print(f"[OK] {label} sync completed.\n")

        except psycopg2.OperationalError as exc:
            print(f"[!] Could not connect to {label} DB: {exc}\n")
        except Exception as exc:
            print(f"[!] ERROR in {label}: {exc}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Upsert media_sources entries from a JSON file into Local and Remote databases."
    )
    parser.add_argument(
        "file",
        help="Path to the JSON file (single object or array of objects).",
    )
    args = parser.parse_args()
    process_file(args.file)
