import psycopg2
from psycopg2 import sql

URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"

translations = {
    "Estación Espacial Internacional (ISS)": "The International Space Station is a research center in low Earth orbit. Its first section was launched into orbit in 1998, and it has been continuously inhabited since November 2000.",
    "Telescopio Espacial Hubble": "Hubble is one of the largest and most versatile space telescopes, famous as a fundamental research tool and public relations advocate for astronomy.",
    "Telescopio Espacial James Webb (JWST)": "The JWST is a space observatory optimized for infrared light, capable of looking back in time to observe the formation of the first galaxies.",
    "Estación Espacial Tiangong": "Tiangong ('Celestial Palace') is a Chinese space station built in low Earth orbit.",
    "Sentinel-2": "Earth observation mission of the Copernicus Program that provides high-resolution optical imagery for terrestrial services (monitoring of vegetation, water, ecosystems).",
    "Starlink (V2 Mini)": "Part of SpaceX's Starlink mega-constellation to provide low-latency global broadband internet.",
    "GPS Block III": "The newest generation of GPS satellites, offering 3x more accuracy and up to 8x better anti-jamming capabilities.",
    "GOES-16 (GOES-East)": "Geostationary meteorological satellite providing the primary weather observation monitoring the American continent and the Atlantic Ocean."
}

def migrate():
    try:
        conn = psycopg2.connect(URL)
        cur = conn.cursor()

        # 1. Add description_en column if it doesn't exist
        print("Checking if description_en column exists...")
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='satellites' AND column_name='description_en';
        """)
        if not cur.fetchone():
            print("Adding description_en column to satellites table...")
            cur.execute("ALTER TABLE satellites ADD COLUMN description_en TEXT;")
            conn.commit()
            print("Column added.")
        else:
            print("Column description_en already exists.")

        # 2. Update existing records
        for name, desc_en in translations.items():
            print(f"Updating satellite: {name}")
            cur.execute(
                "UPDATE satellites SET description_en = %s WHERE name = %s",
                (desc_en, name)
            )
        
        conn.commit()
        print("Migration completed successfully!")
        
        # Verify
        cur.execute("SELECT name, description_en FROM satellites")
        rows = cur.fetchall()
        print("\nVerifying data:")
        for row in rows:
            print(f"- {row[0]}: {row[1][:50]}...")

        cur.close()
        conn.close()

    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    migrate()
