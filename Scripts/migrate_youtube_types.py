import psycopg2
import sys

LOCAL_URL = "postgresql://space_user:space_password@localhost:5433/space_db"
REMOTE_URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"
DB_URLS = [LOCAL_URL, REMOTE_URL]

def migrate():
    for db_url in DB_URLS:
        db_name = "Local" if "localhost" in db_url else "Remote"
        try:
            conn = psycopg2.connect(db_url)
            conn.autocommit = True
            cur = conn.cursor()
        
            # Mapping definitions
            mapping = {
                'channel_spacex': 'new_spacex',
                'channel_news': 'new_space',
                'channel_china_news': 'new_china',
                'launches_starship': 'launches',
                'Lanzamientos': 'launches',
                'Tecnología': 'other',
                'Descubrimiento': 'other'
            }
            
            print(f"[{db_name}] Starting YouTube types migration...")
            
            for old_type, new_type in mapping.items():
                cur.execute(
                    "UPDATE youtube SET type = %s WHERE type = %s",
                    (new_type, old_type)
                )
                if cur.rowcount > 0:
                    print(f"[{db_name}] Updated '{old_type}' to '{new_type}': {cur.rowcount} rows affected")
                
            # Ensure we don't leave any Tecnologia/Descubrimiento даже если у них были немного другие имена
            cur.execute("UPDATE youtube SET type = 'other' WHERE type ILIKE 'tecnologia%' OR type ILIKE 'descubrimiento%'")
            if cur.rowcount > 0:
                print(f"[{db_name}] Cleanup update for similar names: {cur.rowcount} rows affected")

            print(f"[{db_name}] Migration completed successfully.")
            cur.close()
            conn.close()
        except Exception as e:
            print(f"[{db_name}] Error during migration: {e}")


if __name__ == "__main__":
    migrate()
