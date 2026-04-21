import psycopg2

LOCAL_URL = "postgresql://space_user:space_password@localhost:5433/space_db"

def seed():
    try:
        conn = psycopg2.connect(LOCAL_URL)
        conn.autocommit = True
        cur = conn.cursor()
        
        videos = [
            ("Starship IFT-3 Flight", "https://www.youtube.com/watch?v=1pE6Vl95r0A", "launches_starship", "Increíble vuelo de Starship", "Amazing Starship flight", "2024-03-14"),
            ("Falcon 9 Landing", "https://www.youtube.com/watch?v=Z4TXNE5L1zs", "channel_spacex", "Aterrizaje perfecto", "Perfect landing", "2023-12-23"),
            ("James Webb Discovery", "https://www.youtube.com/watch?v=nmMRMvKeb_h", "other", "Nuevas imágenes del universo", "New images of the universe", "2024-01-10"),
        ]
        
        for v in videos:
            cur.execute(
                "INSERT INTO youtube (video_name, url, type, description, description_en, date) VALUES (%s, %s, %s, %s, %s, %s)",
                v
            )
            
        print("Seeded 3 videos successfully")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error seeding: {e}")

if __name__ == "__main__":
    seed()
