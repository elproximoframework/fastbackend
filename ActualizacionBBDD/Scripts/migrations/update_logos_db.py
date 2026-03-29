import psycopg2

URL = "postgresql://space_user:space_password@localhost:5433/space_db"

logo_mapping = {
    "PLD Space": "/logos/pld_space.png",
    "SpaceX": "/logos/spacex.png",
    "ESA": "/logos/esa.png",
    "Rocket Lab": "/logos/rocket_lab.png",
    "Blue Origin": "/logos/blue_origin.png",
    "NASA": "/logos/nasa.png",
    "JAXA": "/logos/jaxa.png",
    "ISRO": "/logos/isro.png",
    "Relativity Space": "/logos/relativity_space.png",
    "Firefly Aerospace": "/logos/firefly.png",
    "CNSA": "/logos/cnsa.png"
}

try:
    conn = psycopg2.connect(URL)
    cur = conn.cursor()
    
    for name, logo_path in logo_mapping.items():
        print(f"Updating {name} with logo {logo_path}...")
        cur.execute("UPDATE companies SET logo = %s WHERE name = %s", (logo_path, name))
    
    conn.commit()
    print("Database updated successfully!")
    conn.close()
except Exception as e:
    print(f"FAILURE: {e}")
