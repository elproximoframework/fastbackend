import psycopg2

LOCAL_URL = "postgresql://space_user:space_password@localhost:5433/space_db"

def seed():
    try:
        conn = psycopg2.connect(LOCAL_URL)
        conn.autocommit = True
        cur = conn.cursor()
        
        videos = [
            ("Starship IFT-3 Flight", "https://www.youtube.com/watch?v=1pE6Vl95r0A", "launches", "Increíble vuelo de Starship", "Amazing Starship flight", "2024-03-14"),
            ("Starship IFT-4 Flight", "https://www.youtube.com/watch?v=SomeID", "launches", "Vuelo IFT-4", "IFT-4 Flight", "2024-06-06"),
            ("SpaceX News Update", "https://www.youtube.com/watch?v=Z4TXNE5L1zs", "new_spacex", "Noticias de SpaceX", "SpaceX News", "2024-04-20"),
            ("China Moon Mission", "https://www.youtube.com/watch?v=SomeID2", "new_china", "Misión lunar china", "China Moon Mission", "2024-05-03"),
            ("James Webb Discovery", "https://www.youtube.com/watch?v=nmMRMvKeb_h", "new_space", "Nuevas imágenes del universo", "New images of the universe", "2024-01-10"),
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
