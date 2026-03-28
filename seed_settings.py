import psycopg2
from psycopg2.extras import Json

# Connection Strings
LOCAL_URL = "postgresql://space_user:space_password@localhost:5433/space_db"

SETTINGS_DATA = [
    {
        "key": "home_video_id",
        "value": "yOITTPvYTl8",
        "type": "string",
        "description": "ID del video de YouTube para la sección principal"
    }
]

def seed_settings(url, db_name):
    print(f"Connecting to {db_name}...")
    try:
        conn = psycopg2.connect(url)
        conn.autocommit = True
        cur = conn.cursor()
        
        print(f"Ensuring table exists and inserting settings in {db_name}...")
        
        # Insert or update settings
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
            
        print(f"Successfully seeded {len(SETTINGS_DATA)} settings in {db_name}!")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error in {db_name}: {e}")

def main():
    seed_settings(LOCAL_URL, "Local DB")

if __name__ == "__main__":
    main()
