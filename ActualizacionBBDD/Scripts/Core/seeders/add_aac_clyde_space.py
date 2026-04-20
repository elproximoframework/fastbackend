import os
import psycopg2
from psycopg2.extras import Json

# Connection URLs
LOCAL_URL = "postgresql://space_user:space_password@localhost:5433/space_db"
REMOTE_URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"

COMPANY_DATA = {
    "name": "AAC Clyde Space",
    "type": "corporate",
    "country": "se",
    "countryName": "Suecia",
    "city": "Uppsala",
    "coordinates": {"lat": 59.8450, "lng": 17.6360},
    "employees": 200,
    "website": "https://www.aac-clyde.space",
    "description": "AAC Clyde Space se especializa en soluciones de datos espaciales, servicios gestionados y plataformas satelitales de alta calidad. La empresa es líder en el mercado de satélites pequeños y medianos (NewSpace), ofreciendo soluciones integrales desde el diseño y fabricación hasta el despliegue y operación en órbita.",
    "description_en": "AAC Clyde Space specializes in small satellite technologies and services that enable businesses, governments, and educational organizations to access high-quality, timely data from space. The company is a leader in the NewSpace market, providing end-to-end solutions.",
    "founded": 2005,
    "ceo": "Luis Gomes",
    "sector": "satellite_manufacturing",
    "tags": ["SmallSats", "CubeSats", "NewSpace", "Services"],
    "socialLinks": {
        "linkedin": "https://www.linkedin.com/company/aac-clyde-space",
        "twitter": "https://twitter.com/aac_clydespace",
        "youtube": "https://www.youtube.com/@Clydespace"
    },
    "keyPrograms": ["xSpancion", "SeaHawk", "EPIC View"],
    "fundingStage": "Public",
    "totalFunding": "N/A",
    "stockTicker": "AAC",
    "otrassede": "Glasgow (UK), London (UK), Hyperion (NL), Omnisys (SE)",
    "show": True
}

def update_db(url, name, item):
    print(f"\n--- Updating {name} Database ---")
    try:
        conn = psycopg2.connect(url)
        conn.autocommit = True
        cur = conn.cursor()
        
        # Check if exists by name
        cur.execute("SELECT id FROM companies WHERE name = %s", (item["name"],))
        existing = cur.fetchone()
        
        if existing:
            print(f"[Updating] {item['name']}...")
            cur.execute("""
                UPDATE companies SET 
                    type=%s, country=%s, "countryName"=%s, city=%s,
                    coordinates=%s, employees=%s, website=%s, description=%s,
                    description_en=%s, founded=%s, ceo=%s, sector=%s,
                    tags=%s, "socialLinks"=%s, "keyPrograms"=%s, "fundingStage"=%s,
                    "totalFunding"=%s, "stockTicker"=%s, otrassede=%s, "show"=%s
                WHERE id=%s
            """, (
                item["type"], item["country"], item["countryName"], item["city"],
                Json(item["coordinates"]), item["employees"], item["website"], item["description"],
                item["description_en"], item["founded"], item["ceo"], item["sector"],
                Json(item["tags"]), Json(item["socialLinks"]), Json(item["keyPrograms"]), item["fundingStage"],
                item["totalFunding"], item["stockTicker"], item["otrassede"], item["show"],
                existing[0]
            ))
        else:
            print(f"[Inserting] {item['name']}...")
            cur.execute("""
                INSERT INTO companies (
                    name, type, country, "countryName", city,
                    coordinates, employees, website, description,
                    description_en, founded, ceo, sector,
                    tags, "socialLinks", "keyPrograms", "fundingStage",
                    "totalFunding", "stockTicker", otrassede, "show"
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                item["name"], item["type"], item["country"], item["countryName"], item["city"],
                Json(item["coordinates"]), item["employees"], item["website"], item["description"],
                item["description_en"], item["founded"], item["ceo"], item["sector"],
                Json(item["tags"]), Json(item["socialLinks"]), Json(item["keyPrograms"]), item["fundingStage"],
                item["totalFunding"], item["stockTicker"], item["otrassede"], item["show"]
            ))
        
        cur.close()
        conn.close()
        print(f"[✓] {name} update complete.")
    except Exception as e:
        print(f"[!] ERROR in {name}: {e}")

if __name__ == "__main__":
    # Update Local
    update_db(LOCAL_URL, "Local", COMPANY_DATA)
    # Update Remote
    update_db(REMOTE_URL, "Remote", COMPANY_DATA)
