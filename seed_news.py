import psycopg2
import sys
import json
from psycopg2.extras import Json

# Connection Strings
LOCAL_URL = "postgresql://space_user:space_password@localhost:5433/space_db"
REMOTE_URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"

NEWS_DATA = [
    {
        "id": 1,
        "title": "La ESA anuncia nueva misión para estudiar asteroides cercanos",
        "title_en": "ESA announces new mission to study near-Earth asteroids",
        "excerpt": "La Agencia Espacial Europea ha revelado planes para lanzar una nueva sonda destinada a estudiar asteroides potencialmente peligrosos.",
        "excerpt_en": "The European Space Agency has revealed plans to launch a new probe aimed at studying potentially hazardous asteroids.",
        "body": "Contenido completo sobre la misión de la ESA para estudiar asteroides cercanos...",
        "body_en": "Full content about the ESA mission to study near-Earth asteroids...",
        "category": "Agencias",
        "category_en": "Agencies",
        "location": "Europa",
        "location_en": "Europe",
        "covered": True,
        "date": "2026-03-27T10:00:00Z",
        "image": "/assets/imagesnew/esa_asteroids.png",
        "slug": "esa-nueva-mision-asteroides",
        "tags": ["ESA", "Asteroides", "Misión", "Defensa Planetaria"],
        "tags_en": ["ESA", "Asteroids", "Mission", "Planetary Defense"],
        "featured": True,
        "linkyoutube": "https://www.youtube.com/watch?v=d_1NbMY9uic",
        "rutanoticia": "/api/v1/news_content/noticia1.md",
        "timestart": 65
    },
    {
        "id": 2,
        "title": "SpaceX completa exitosamente la quinta prueba de Starship",
        "title_en": "SpaceX successfully completes fifth Starship test flight",
        "excerpt": "El cohete más grande de la historia alcanzó la órbita deseada y logró amerizar de forma controlada en el océano Índico.",
        "excerpt_en": "The largest rocket in history reached its desired orbit and achieved a controlled splashdown in the Indian Ocean.",
        "body": "Detalles completos de la quinta prueba orbital de Starship...",
        "body_en": "Full details of the fifth Starship orbital test...",
        "category": "SpaceX",
        "category_en": "SpaceX",
        "location": "EEUU",
        "location_en": "USA",
        "covered": True,
        "date": "2026-03-27T08:30:00Z",
        "image": "/assets/imagesnew/starship_test.png",
        "slug": "spacex-exito-quinta-prueba-starship",
        "tags": ["SpaceX", "Starship", "Lanzamiento", "Reutilizable"],
        "tags_en": ["SpaceX", "Starship", "Launch", "Reusable"],
        "featured": True,
        "linkyoutube": "https://www.youtube.com/watch?v=d_1NbMY9uic",
        "rutanoticia": "/api/v1/news_content/noticia2.md",
        "timestart": 220
    },
    {
        "id": 3,
        "title": "El Telescopio James Webb descubre moléculas de agua en exoplaneta",
        "title_en": "James Webb Telescope discovers water molecules on exoplanet",
        "excerpt": "Nuevas observaciones apuntan a la existencia de un mundo acuático a 120 años luz de la Tierra, reavivando las esperanzas de encontrar vida.",
        "excerpt_en": "New observations point to the existence of a water world 120 light years from Earth, rekindling hopes of finding life.",
        "body": "Análisis completo de los datos del telescopio James Webb...",
        "body_en": "Full analysis of James Webb telescope data...",
        "category": "Ciencia",
        "category_en": "Science",
        "location": "Resto",
        "location_en": "Rest",
        "covered": False,
        "date": "2026-03-26T15:45:00Z",
        "image": "/assets/imagesnew/jwst_water.png",
        "slug": "james-webb-descubre-agua-exoplaneta",
        "tags": ["JWST", "Exoplanetas", "Agua", "Astrobiología"],
        "tags_en": ["JWST", "Exoplanetas", "Water", "Astrobiology"],
        "featured": False,
        "linkyoutube": None,
        "rutanoticia": "/api/v1/news_content/noticia3.md",
        "timestart": None
    }
]

def seed_db(url, db_name):
    print(f"Connecting to {db_name}...")
    try:
        conn = psycopg2.connect(url)
        conn.autocommit = True
        cur = conn.cursor()
        
        print(f"Clearing existing news in {db_name}...")
        cur.execute("TRUNCATE TABLE news RESTART IDENTITY CASCADE;")
        
        print(f"Inserting news data in {db_name}...")
        insert_query = """
        INSERT INTO news (
            title, title_en, excerpt, excerpt_en, body, body_en,
            category, category_en, location, location_en, covered,
            date, image, slug, tags, tags_en, featured,
            linkyoutube, rutanoticia, timestart
        ) VALUES (
            %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s,
            %s, %s, %s
        )
        """
        
        for news in NEWS_DATA:
            cur.execute(insert_query, (
                news["title"], news["title_en"], news["excerpt"], news["excerpt_en"],
                news["body"], news["body_en"], news["category"], news["category_en"],
                news["location"], news["location_en"], news["covered"],
                news["date"], news["image"], news["slug"], Json(news["tags"]),
                Json(news["tags_en"]), news["featured"], news["linkyoutube"],
                news["rutanoticia"], news["timestart"]
            ))
            
        print(f"Successfully seeded {len(NEWS_DATA)} news items in {db_name}!")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error in {db_name}: {e}")

def main():
    seed_db(LOCAL_URL, "Local DB")
    seed_db(REMOTE_URL, "Remote DB (Railway)")

if __name__ == "__main__":
    main()
