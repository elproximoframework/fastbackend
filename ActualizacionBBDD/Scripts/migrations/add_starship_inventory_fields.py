"""
Migration: Add Starship structured data fields to spacex_inventory table.

New columns:
  - serial_number  VARCHAR  (e.g. "SN15", "B7", "R3-SN1")
  - block          VARCHAR  (e.g. "Block 1", "Block 2", "Block 3")
  - specs          JSONB    (technical parameters: thrust, Isp, mass, etc.)
  - flight_data    JSONB    (IFT flight outcome per stage)
  - milestones     JSONB    (list of {date, event} dicts)

Run with:
    python d:\\YoutubeElProximoFrameworkEnElEspacio\\Web\\backendfast\\ActualizacionBBDD\\Scripts\\migrations\\add_starship_inventory_fields.py
"""

import psycopg2

LOCAL_URL  = "postgresql://space_user:space_password@localhost:5433/space_db"
REMOTE_URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"

MIGRATIONS = [
    "ALTER TABLE spacex_inventory ADD COLUMN IF NOT EXISTS serial_number VARCHAR;",
    "ALTER TABLE spacex_inventory ADD COLUMN IF NOT EXISTS block VARCHAR;",
    "ALTER TABLE spacex_inventory ADD COLUMN IF NOT EXISTS specs JSONB;",
    "ALTER TABLE spacex_inventory ADD COLUMN IF NOT EXISTS flight_data JSONB;",
    "ALTER TABLE spacex_inventory ADD COLUMN IF NOT EXISTS milestones JSONB;",
]

def run_migrations(label: str, url: str):
    print(f"\n--- Running migrations on {label} ---")
    try:
        conn = psycopg2.connect(url)
        conn.autocommit = True
        cur = conn.cursor()
        for stmt in MIGRATIONS:
            try:
                cur.execute(stmt)
                print(f"  [✓] {stmt.strip()[:70]}")
            except Exception as e:
                print(f"  [!] FAILED: {stmt.strip()[:70]}")
                print(f"      Error: {e}")
        cur.close()
        conn.close()
        print(f"[OK] {label} migration completed.")
    except Exception as e:
        print(f"[!] Could not connect to {label}: {e}")

if __name__ == "__main__":
    run_migrations("Local", LOCAL_URL)
    run_migrations("Remote (Railway)", REMOTE_URL)
