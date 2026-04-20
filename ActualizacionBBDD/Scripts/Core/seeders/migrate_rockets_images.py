import psycopg2

LOCAL_URL = "postgresql://space_user:space_password@localhost:5433/space_db"

def migrate_rockets():
    mapping = {
        'Falcon 9': '/api/v1/rocket_images/falcon9.png',
        'Starship': '/api/v1/rocket_images/starship.png',
        'Electron': '/api/v1/rocket_images/electron.png',
        'Ariane 6': '/api/v1/rocket_images/ariane6.png',
        'Miura 5': '/api/v1/rocket_images/miura5.png',
        'SLS': '/api/v1/rocket_images/sls.png',
        'New Glenn': '/api/v1/rocket_images/new_glenn.png',
        'Vega-C': '/api/v1/rocket_images/vegac.png',
        'Miura 1': '/api/v1/rocket_images/miura5.png' # Fallback to Miura 5 image for now
    }

    try:
        conn = psycopg2.connect(LOCAL_URL)
        cur = conn.cursor()
        
        for name, path in mapping.items():
            cur.execute("UPDATE rockets SET image = %s WHERE name ILIKE %s;", (path, f"%{name}%"))
            print(f"Updated {name} to {path}")
            
        conn.commit()
        cur.close()
        conn.close()
        print("Migration completed successfully.")
    except Exception as e:
        print(f"Error during migration: {e}")

if __name__ == "__main__":
    migrate_rockets()
