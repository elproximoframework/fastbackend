import os
import psycopg2
from psycopg2.extras import Json
from datetime import datetime

# Connection URLs
LOCAL_URL = "postgresql://space_user:space_password@localhost:5433/space_db"
REMOTE_URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"

# Metadata for Project Sunrise
# Content is read from Markdown files referenced in rutanoticia
NEWS_ITEM = {
    "title": "Informe Técnico: Project Sunrise — Blue Origin y los Centros de Datos Orbitales",
    "title_en": "Technical Report: Project Sunrise — Blue Origin and Orbital Data Centers",
    "excerpt": "Blue Origin ha solicitado permiso a la FCC para desplegar Project Sunrise, una constelación de 51.600 satélites que actuarán como centros de datos en órbita, aprovechando el vacío para la refrigeración y el sol para energía inagotable.",
    "excerpt_en": "The explosion in peak demand for artificial intelligence computing is saturating terrestrial infrastructure. In this context, Blue Origin proposes Project Sunrise, a constellation of orbital data centers.",
    "category": "Sector Privado",
    "category_en": "Private Sector",
    "location": "EEUU",
    "location_en": "USA",
    "covered": True,
    "date": "2026-03-28T10:00:00Z",
    "image": "blue_origin_sunrise.png",
    "slug": "informe-tecnico-project-sunrise-blue-origin",
    "tags": ["Blue Origin", "Project Sunrise", "Centros de Datos", "IA", "Satélites"],
    "tags_en": ["Blue Origin", "Project Sunrise", "Data Centers", "AI", "Satellites"],
    "featured": True,
    "linkyoutube": "https://youtu.be/wPkO3TPnlAE",
    "timestart": 674,
    "rutanoticia": "/api/v1/news_content/260328_informe_tecnico_blue_origin_sunrise.md",
    "show": True
}

def update_db(url, name, item):
    print(f"\n--- Updating {name} Database ---")
    try:
        conn = psycopg2.connect(url)
        conn.autocommit = True
        cur = conn.cursor()
        
        # Check if exists by slug
        cur.execute("SELECT id FROM news WHERE slug = %s", (item["slug"],))
        existing = cur.fetchone()
        
        if existing:
            print(f"[Updating] {item['slug']}...")
            cur.execute("""
                UPDATE news SET 
                    title=%s, title_en=%s, excerpt=%s, excerpt_en=%s,
                    category=%s, category_en=%s, location=%s, location_en=%s,
                    covered=%s, date=%s, image=%s, tags=%s, tags_en=%s,
                    featured=%s, linkyoutube=%s, timestart=%s, rutanoticia=%s, "show"=%s
                WHERE slug=%s
            """, (
                item["title"], item["title_en"], item["excerpt"], item["excerpt_en"],
                item["category"], item["category_en"], item["location"], item["location_en"],
                item["covered"], item["date"], item["image"], Json(item["tags"]), Json(item["tags_en"]),
                item["featured"], item["linkyoutube"], item["timestart"], item["rutanoticia"], item["show"],
                item["slug"]
            ))
        else:
            print(f"[Inserting] {item['slug']}...")
            cur.execute("""
                INSERT INTO news (
                    title, title_en, excerpt, excerpt_en,
                    category, category_en, location, location_en,
                    covered, date, image, slug, tags, tags_en,
                    featured, linkyoutube, timestart, rutanoticia, "show"
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                item["title"], item["title_en"], item["excerpt"], item["excerpt_en"],
                item["category"], item["category_en"], item["location"], item["location_en"],
                item["covered"], item["date"], item["image"], item["slug"], Json(item["tags"]), Json(item["tags_en"]),
                item["featured"], item["linkyoutube"], item["timestart"], item["rutanoticia"], item["show"]
            ))
        
        cur.close()
        conn.close()
        print(f"[✓] {name} update complete.")
    except Exception as e:
        print(f"[!] ERROR in {name}: {e}")

if __name__ == "__main__":
    # Update Local
    update_db(LOCAL_URL, "Local", NEWS_ITEM)
    # Update Remote
    update_db(REMOTE_URL, "Remote", NEWS_ITEM)
