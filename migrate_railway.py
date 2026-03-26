import psycopg2
import os

# Use DATABASE_URL from environment, fallback to local for testing
URL = os.environ.get("DATABASE_URL", "postgresql://space_user:space_password@localhost:5433/space_db")

translations = {
    "Estación Espacial Internacional (ISS)": "It orbits the Earth every 90 minutes, meaning astronauts see 16 sunrises and sunsets every day.",
    "Telescopio Espacial Hubble": "Despite its incredible astrophysical discoveries, it was originally launched with a defective mirror that had to be repaired in orbit in 1993.",
    "Telescopio Espacial James Webb (JWST)": "It operates at an incredible -223°C (50 Kelvin) and features a sunshield the size of a tennis court.",
    "Estación Espacial Tiangong": "It is the culmination of a 30-year Chinese space program, assembled entirely independently by the country.",
    "Sentinel-2": "It maps the entirety of our planet's land surface and large coastal areas typically every 5 days.",
    "Starlink (V2 Mini)": "V2 Mini satellites features argon Hall-effect thrusters, which are cheaper and more efficient than the previous version.",
    "GPS Block III": "A GPS satellite constantly transmits a radio signal with its position and the exact time; in reality, all of GPS is just measuring how long it takes for light to reach you.",
    "GOES-16 (GOES-East)": "Being in GEO orbit, it appears to stay at the same point over the equator because its orbital period exactly matches the Earth's rotation (1 day)."
}

def migrate():
    if "localhost" not in URL:
        print("!!! RUNNING ON PRODUCTION DATABASE (Non-localhost URL detected) !!!")
    
    try:
        conn = psycopg2.connect(URL)
        cur = conn.cursor()

        # 1. Add funFact_en column if it doesn't exist
        print("Checking if funFact_en column exists...")
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='satellites' AND column_name='funFact_en';
        """)
        if not cur.fetchone():
            print("Adding funFact_en column to satellites table...")
            cur.execute('ALTER TABLE satellites ADD COLUMN "funFact_en" TEXT;')
            conn.commit()
            print("Column added.")
        else:
            print("Column funFact_en already exists.")

        # 2. Update existing records
        for name, fun_en in translations.items():
            print(f"Updating satellite: {name}")
            cur.execute(
                'UPDATE satellites SET "funFact_en" = %s WHERE name = %s',
                (fun_en, name)
            )
        
        conn.commit()
        print("Migration completed successfully!")
        
        # Verify
        cur.execute('SELECT name, "funFact_en" FROM satellites')
        rows = cur.fetchall()
        print("\nVerifying data:")
        for row in rows:
            print(f"- {row[0]}: {row[1][:50] if row[1] else 'NULL'}...")

        cur.close()
        conn.close()

    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    migrate()
