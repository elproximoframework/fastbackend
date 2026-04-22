import psycopg2
import sys

DATABASE_URL = "postgresql://space_user:space_password@localhost:5433/space_db"

def migrate():
    try:
        conn = psycopg2.connect(DATABASE_URL)
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
        
        print("Starting YouTube types migration...")
        
        for old_type, new_type in mapping.items():
            cur.execute(
                "UPDATE youtube SET type = %s WHERE type = %s",
                (new_type, old_type)
            )
            print(f"Updated '{old_type}' to '{new_type}': {cur.rowcount} rows affected")
            
        # Ensure we don't leave any Tecnologia/Descubrimiento even if they had slightly different names
        cur.execute("UPDATE youtube SET type = 'other' WHERE type ILIKE 'tecnologia%' OR type ILIKE 'descubrimiento%'")
        if cur.rowcount > 0:
            print(f"Cleanup update for similar names: {cur.rowcount} rows affected")

        print("Migration completed successfully.")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error during migration: {e}")
        sys.exit(1)

if __name__ == "__main__":
    migrate()
