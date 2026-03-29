import psycopg2
import os

# Remote Connection String (from migrate_railway.py)
REMOTE_URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"

SETTINGS_DATA = [
    {
        "key": "home_video_id",
        "value": "yOITTPvYTl8",
        "type": "string",
        "description": "ID del video de YouTube para la sección principal"
    }
]

def sync_remote():
    print(f"Connecting to Remote DB: {REMOTE_URL.split('@')[-1]}...")
    try:
        conn = psycopg2.connect(REMOTE_URL)
        conn.autocommit = False # Using manual commit for multiple steps
        cur = conn.cursor()

        # 1. Create app_settings table
        print("Ensuring 'app_settings' table exists in Remote...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS app_settings (
                id SERIAL PRIMARY KEY,
                key VARCHAR(255) UNIQUE NOT NULL,
                value TEXT NOT NULL,
                type VARCHAR(50) DEFAULT 'string',
                description TEXT
            );
        """)
        
        # 2. Seed app_settings data
        print("Seeding 'app_settings' data...")
        insert_query = """
            INSERT INTO app_settings (key, value, type, description)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (key) DO UPDATE SET
                value = EXCLUDED.value,
                type = EXCLUDED.type,
                description = EXCLUDED.description;
        """
        for setting in SETTINGS_DATA:
            cur.execute(insert_query, (
                setting["key"], 
                setting["value"], 
                setting["type"], 
                setting["description"]
            ))

        # 3. Drop 'logo' column from 'companies' if it exists (to match Local)
        print("Dropping 'logo' column from 'companies' table (to match Local)...")
        cur.execute("ALTER TABLE companies DROP COLUMN IF EXISTS logo;")

        # 4. Unify types (Convert VARCHAR to TEXT to match Local)
        # Note: TEXT and VARCHAR are interchangeable in PG, but this removes the comparison "noise"
        print("Converting VARCHAR columns to TEXT for consistency...")
        type_conversions = [
            ("rockets", "description"),
            ("satellites", "description"),
            ("satellites", "funFact"),
            ("launches", "mission_description"),
            ("companies", "description")
        ]
        
        for table, col in type_conversions:
            print(f"  - Altering {table}.{col} to TEXT")
            # Using ALTER TABLE ... ALTER COLUMN ... TYPE TEXT
            # psycopg2 handles identifiers better if quoted
            cur.execute(f'ALTER TABLE {table} ALTER COLUMN "{col}" TYPE TEXT;')

        conn.commit()
        print("\n[✓] Remote DB updated successfully!")
        
        cur.close()
        conn.close()

    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
        print(f"\n[!] ERROR during synchronization: {e}")

if __name__ == "__main__":
    sync_remote()
