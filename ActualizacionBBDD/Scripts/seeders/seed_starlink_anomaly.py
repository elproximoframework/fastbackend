import psycopg2
import json

# Connection Strings
LOCAL_URL = "postgresql://space_user:space_password@localhost:5433/space_db"
REMOTE_URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"

NEWS_DATA = {
    "title": "Anomalía en Órbita de Satélite Starlink y Reconfiguración de la Constelación",
    "title_en": "Starlink Orbital Anomaly and Constellation Reconfiguration",
    "excerpt": "SpaceX ha informado que el satélite Starlink 34343 experimentó una anomalía en órbita el pasado domingo, lo que resultó en una pérdida total de comunicaciones...",
    "excerpt_en": "SpaceX has reported that Starlink satellite 34343 experienced an on-orbit anomaly last Sunday, resulting in a total loss of communications...",
    "category": "Starlink",
    "category_en": "Starlink",
    "location": "Otros",
    "location_en": "Others",
    "date": "2026-03-29",
    "image": "starlink_anomaly_2026.png",
    "slug": "anomalia-orbita-satelite-starlink-reconfiguracion-constelacion",
    "tags": ["Starlink", "SpaceX", "Basura Espacial"],
    "tags_en": ["Starlink", "SpaceX", "Space Debris"],
    "featured": True,
    "rutanoticia": "/api/v1/newsspacex_content/260329_starlink_anomaly.md",
    "show": True
}

def seed_db(url, name):
    print(f"Connecting to {name} DB...")
    try:
        conn = psycopg2.connect(url)
        cur = conn.cursor()

        print(f"Inserting/Updating news item in {name} 'newsspacex' table...")
        insert_query = """
            INSERT INTO newsspacex (
                title, title_en, excerpt, excerpt_en, category, category_en, 
                location, location_en, covered, date, image, slug, tags, tags_en, 
                featured, rutanoticia, show
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (slug) DO UPDATE SET
                title = EXCLUDED.title,
                title_en = EXCLUDED.title_en,
                excerpt = EXCLUDED.excerpt,
                excerpt_en = EXCLUDED.excerpt_en,
                category = EXCLUDED.category,
                category_en = EXCLUDED.category_en,
                location = EXCLUDED.location,
                location_en = EXCLUDED.location_en,
                covered = EXCLUDED.covered,
                date = EXCLUDED.date,
                image = EXCLUDED.image,
                tags = EXCLUDED.tags,
                tags_en = EXCLUDED.tags_en,
                featured = EXCLUDED.featured,
                rutanoticia = EXCLUDED.rutanoticia,
                show = EXCLUDED.show;
        """
        
        cur.execute(insert_query, (
            NEWS_DATA["title"], NEWS_DATA["title_en"], 
            NEWS_DATA["excerpt"], NEWS_DATA["excerpt_en"],
            NEWS_DATA["category"], NEWS_DATA["category_en"],
            NEWS_DATA["location"], NEWS_DATA["location_en"],
            NEWS_DATA.get("covered", False),
            NEWS_DATA["date"], NEWS_DATA["image"],
            NEWS_DATA["slug"], json.dumps(NEWS_DATA["tags"]), json.dumps(NEWS_DATA["tags_en"]),
            NEWS_DATA["featured"], NEWS_DATA["rutanoticia"], NEWS_DATA["show"]
        ))

        conn.commit()
        print(f"[✓] {name} DB updated successfully!")
        
        cur.close()
        conn.close()

    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
        print(f"[!] ERROR in {name} DB: {e}")

if __name__ == "__main__":
    seed_db(LOCAL_URL, "Local")
    seed_db(REMOTE_URL, "Remote")
