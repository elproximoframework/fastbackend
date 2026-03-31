import psycopg2
import os

# Remote Connection String
REMOTE_URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"

def migrate_remote():
    print(f"Connecting to Remote DB to create 'newsspacex' table...")
    try:
        conn = psycopg2.connect(REMOTE_URL)
        cur = conn.cursor()

        print("Creating 'newsspacex' table in Remote...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS newsspacex (
                id SERIAL PRIMARY KEY,
                title VARCHAR NOT NULL,
                title_en VARCHAR,
                excerpt TEXT,
                excerpt_en TEXT,
                category VARCHAR,
                category_en VARCHAR,
                location VARCHAR,
                location_en VARCHAR,
                covered BOOLEAN DEFAULT FALSE,
                date VARCHAR,
                image VARCHAR,
                slug VARCHAR UNIQUE,
                tags JSONB,
                tags_en JSONB,
                featured BOOLEAN DEFAULT FALSE,
                linkyoutube VARCHAR,
                rutanoticia VARCHAR,
                timestart INTEGER,
                show BOOLEAN DEFAULT TRUE
            );
        """)

        print("Creating indexes...")
        cur.execute("CREATE INDEX IF NOT EXISTS ix_newsspacex_id ON newsspacex (id);")
        cur.execute("CREATE INDEX IF NOT EXISTS ix_newsspacex_title ON newsspacex (title);")
        cur.execute("CREATE INDEX IF NOT EXISTS ix_newsspacex_title_en ON newsspacex (title_en);")
        cur.execute("CREATE INDEX IF NOT EXISTS ix_newsspacex_category ON newsspacex (category);")
        cur.execute("CREATE INDEX IF NOT EXISTS ix_newsspacex_category_en ON newsspacex (category_en);")
        cur.execute("CREATE INDEX IF NOT EXISTS ix_newsspacex_slug ON newsspacex (slug);")

        conn.commit()
        print("\n[✓] Remote 'newsspacex' table created successfully!")
        
        cur.close()
        conn.close()

    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
        print(f"\n[!] ERROR during remote migration: {e}")

if __name__ == "__main__":
    migrate_remote()
