import os
import re
import psycopg2
from psycopg2.extras import Json
from datetime import datetime

# Connection URLs
LOCAL_URL = "postgresql://space_user:space_password@localhost:5433/space_db"
REMOTE_URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"
NEWS_DIR = "news"

IMAGE_MAPPING = {
    "260328_informe_tecnico_china_lunar.md": "china_lunar_921.png",
    "260328_informe_tecnico_esa_epic.md": "esa_asteroids.png",
    "260328_informe_tecnico_transastra_capture_bag.md": "inflatable_habitat.png",
    "260328_informe_tecnico_wispit2_protoplanetas.md": "jwst_water.png",
    "260328_informe_tecnico_blue_origin_sunrise.md": "miura5_factory.png", # Placeholder
    "260328_informe_tecnico_isar_spectrum.md": "electron_recovery.png", # Placeholder
    "260328_informe_tecnico_nasa_ignition.md": "plasma_engine.png", # Placeholder
    "260328_informe_tecnico_roman_space_telescope.md": "jwst_water.png", # Placeholder
    "260328_informe_tecnico_cometa_atlas_k1.md": "default_news.png",
    "260328_informe_tecnico_cielo_marzo_2026.md": "default_news.png"
}
DEFAULT_IMAGE = "default_news.png"

def get_excerpt(content):
    # Find the first paragraph that isn't a header or metadata
    lines = content.split('\n')
    for line in lines:
        line = line.strip()
        if not line: continue
        if line.startswith('#'): continue
        if line.startswith('**'): continue
        if line.startswith('---'): continue
        if line.startswith('>'): continue
        if len(line) > 50: # Assume it's a descriptive paragraph
            # Clean markdown formatting for excerpt
            excerpt = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', line)
            excerpt = re.sub(r'\*\*(.*?)\*\*', r'\1', excerpt)
            excerpt = re.sub(r'\*(.*?)\*', r'\1', excerpt)
            return excerpt[:200] + '...' if len(excerpt) > 200 else excerpt
    return ""

def process_news():
    news_items = []
    if not os.path.exists(NEWS_DIR):
        print(f"Directory {NEWS_DIR} not found.")
        return []
        
    files = [f for f in os.listdir(NEWS_DIR) if f.endswith('.md') and not f.endswith('_en.md') and 'informe_tecnico' in f]
    
    for filename in files:
        filepath = os.path.join(NEWS_DIR, filename)
        en_filename = filename.replace('.md', '_en.md')
        en_filepath = os.path.join(NEWS_DIR, en_filename)
        
        if not os.path.exists(en_filepath):
            print(f"English version not found for {filename}")
            continue
            
        with open(filepath, 'r', encoding='utf-8') as f:
            es_content = f.read()
        with open(en_filepath, 'r', encoding='utf-8') as f:
            en_content = f.read()
            
        # Extract title
        es_title_match = re.search(r'^#\s+(.*)', es_content, re.MULTILINE)
        es_title = es_title_match.group(1) if es_title_match else filename
        
        en_title_match = re.search(r'^#\s+(.*)', en_content, re.MULTILINE)
        en_title = en_title_match.group(1) if en_title_match else es_title
        
        # Extract excerpt
        es_excerpt = get_excerpt(es_content)
        en_excerpt = get_excerpt(en_content)
        
        # Extract date from filename: 260328_... -> 2026-03-28
        date_match = re.search(r'^(\d{2})(\d{2})(\d{2})', filename)
        if date_match:
            yy, mm, dd = date_match.groups()
            date_str = f"20{yy}-{mm}-{dd}T10:00:00Z"
        else:
            date_str = datetime.now().strftime("%Y-%m-%dT10:00:00Z")
            
        # Slug
        slug = filename.replace('.md', '').replace('_', '-')
        
        news_items.append({
            "title": es_title,
            "title_en": en_title,
            "excerpt": es_excerpt,
            "excerpt_en": en_excerpt,
            "category": "Informes Técnicos",
            "category_en": "Technical Reports",
            "location": "Global",
            "location_en": "Global",
            "covered": True,
            "date": date_str,
            "image": IMAGE_MAPPING.get(filename, DEFAULT_IMAGE),
            "slug": slug,
            "tags": ["Informe Técnico", "Espacio"],
            "tags_en": ["Technical Report", "Space"],
            "featured": False,
            "rutanoticia": f"/api/v1/news_content/{filename}",
            "show": True
        })
    return news_items

def update_db(url, name, items):
    print(f"\n--- Updating {name} Database ---")
    try:
        conn = psycopg2.connect(url)
        conn.autocommit = True
        cur = conn.cursor()
        
        for item in items:
            # Check if exists by slug
            cur.execute("SELECT id FROM news WHERE slug = %s", (item["slug"],))
            existing = cur.fetchone()
            
            if existing:
                print(f"[Updating] {item['slug']}...")
                cur.execute("""
                    UPDATE news SET 
                        title=%s, title_en=%s, excerpt=%s, excerpt_en=%s,
                        category=%s, category_en=%s, location=%s, location_en=%s,
                        covered=%s, date=%s, rutanoticia=%s, "show"=%s,
                        tags=%s, tags_en=%s, image=%s
                    WHERE slug=%s
                """, (
                    item["title"], item["title_en"], item["excerpt"], item["excerpt_en"],
                    item["category"], item["category_en"], item["location"], item["location_en"],
                    item["covered"], item["date"], item["rutanoticia"], item["show"],
                    Json(item["tags"]), Json(item["tags_en"]), item["image"],
                    item["slug"]
                ))
            else:
                print(f"[Inserting] {item['slug']}...")
                cur.execute("""
                    INSERT INTO news (
                        title, title_en, excerpt, excerpt_en,
                        category, category_en, location, location_en,
                        covered, date, slug, tags, tags_en,
                        featured, rutanoticia, "show", image
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    item["title"], item["title_en"], item["excerpt"], item["excerpt_en"],
                    item["category"], item["category_en"], item["location"], item["location_en"],
                    item["covered"], item["date"], item["slug"], Json(item["tags"]),
                    Json(item["tags_en"]), item["featured"], item["rutanoticia"], item["show"],
                    item["image"]
                ))
        
        cur.close()
        conn.close()
        print(f"[✓] {name} update complete.")
    except Exception as e:
        print(f"[!] ERROR in {name}: {e}")

if __name__ == "__main__":
    # Ensure we are in the right directory if running from somewhere else
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    items = process_news()
    print(f"Processed {len(items)} news items from '{NEWS_DIR}/' directory.")
    
    if not items:
        print("No news items found to update.")
    else:
        # Update Local
        update_db(LOCAL_URL, "Local", items)
        # Update Remote
        update_db(REMOTE_URL, "Remote", items)
