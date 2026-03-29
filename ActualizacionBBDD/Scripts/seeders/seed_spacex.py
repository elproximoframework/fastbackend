import os
import json
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# SpaceX Data
spacex_data = {
    "name": "SpaceX",
    "type": "contractor",
    "country": "us",
    "countryName": "Estados Unidos",
    "city": "Hawthorne",
    "coordinates": json.dumps({ "lat": 33.9213, "lng": -118.3267 }),
    "employees": 18150,
    "website": "https://www.spacex.com",
    "description": "SpaceX diseña, fabrica y lanza avanzados cohetes y naves espaciales. La compañía fue fundada en 2002 para revolucionar la tecnología espacial, con el objetivo final de permitir a la gente vivir en otros planetas.",
    "description_en": "SpaceX designs, manufactures and launches advanced rockets and spacecraft. The company was founded in 2002 to revolutionize space technology, with the ultimate goal of enabling people to live on other planets.",
    "founded": 2002,
    "ceo": "Elon Musk",
    "sector": "launchers",
    "tags": json.dumps(["Starship", "Falcon 9", "Starlink", "Mars", "Reusability"]),
    "socialLinks": json.dumps({
        "twitter": "https://twitter.com/spacex",
        "linkedin": "https://www.linkedin.com/company/spacex",
        "youtube": "https://www.youtube.com/spacex"
    }),
    "keyPrograms": json.dumps(["Starship", "Falcon 9", "Starlink", "Dragon"]),
    "fundingStage": "Late Stage",
    "totalFunding": "$11.9B",
    "stockTicker": None,
    "show": True
}

db_urls = [
    ("Local", "postgresql://space_user:space_password@localhost:5433/space_db"),
    ("Railway", "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway")
]

def seed_database(name, url):
    print(f"--- Seeding {name} Database ---")
    try:
        engine = create_engine(url)
        Session = sessionmaker(bind=engine)
        session = Session()

        # Check if SpaceX already exists
        result = session.execute(text("SELECT id FROM companies WHERE name = 'SpaceX'")).fetchone()
        
        if result:
            print(f"Updating SpaceX in {name}...")
            update_query = text("""
                UPDATE companies 
                SET type = :type, country = :country, "countryName" = :countryName, city = :city, 
                    coordinates = :coordinates, employees = :employees, website = :website, 
                    description = :description, description_en = :description_en, founded = :founded, 
                    ceo = :ceo, sector = :sector, tags = :tags, "socialLinks" = :socialLinks, 
                    "keyPrograms" = :keyPrograms, "fundingStage" = :fundingStage, 
                    "totalFunding" = :totalFunding, "stockTicker" = :stockTicker, show = :show
                WHERE name = 'SpaceX'
            """)
            session.execute(update_query, {**spacex_data, "name": "SpaceX"})
        else:
            print(f"Inserting SpaceX into {name}...")
            insert_query = text("""
                INSERT INTO companies (
                    name, type, country, "countryName", city, coordinates, employees, website, 
                    description, description_en, founded, ceo, sector, tags, "socialLinks", 
                    "keyPrograms", "fundingStage", "totalFunding", "stockTicker", show
                ) VALUES (
                    :name, :type, :country, :countryName, :city, :coordinates, :employees, :website, 
                    :description, :description_en, :founded, :ceo, :sector, :tags, :socialLinks, 
                    :keyPrograms, :fundingStage, :totalFunding, :stockTicker, :show
                )
            """)
            session.execute(insert_query, spacex_data)
        
        session.commit()
        print(f"Successfully seeded SpaceX in {name}!")
        session.close()
    except Exception as e:
        print(f"Error seeding {name}: {e}")

if __name__ == "__main__":
    for name, url in db_urls:
        seed_database(name, url)
