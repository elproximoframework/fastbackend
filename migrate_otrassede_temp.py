from sqlalchemy import create_engine, text
import sys

local_url = "postgresql://space_user:space_password@localhost:5433/space_db"
remote_url = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"

def migrate(url, name):
    print(f"Migrating {name}...")
    try:
        engine = create_engine(url)
        with engine.connect() as conn:
            conn.execute(text("ALTER TABLE companies ADD COLUMN IF NOT EXISTS otrassede VARCHAR;"))
            conn.commit()
            print(f"Successfully migrated {name}")
    except Exception as e:
        print(f"Error migrating {name}: {e}")

if __name__ == "__main__":
    migrate(local_url, "Local")
    migrate(remote_url, "Remote")
