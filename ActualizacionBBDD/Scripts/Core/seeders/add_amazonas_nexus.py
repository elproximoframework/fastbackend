import json
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from datetime import date

# Database URLs
db_urls = [
    ("Local", "postgresql://space_user:space_password@localhost:5433/space_db"),
    ("Railway", "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway")
]

# Hispasat Data
hispasat_data = {
    "name": "Hispasat",
    "type": "operator",
    "country": "es",
    "countryName": "España",
    "city": "Madrid",
    "coordinates": json.dumps({"lat": 40.4168, "lng": -3.7038}),
    "employees": 200,
    "website": "https://www.hispasat.com",
    "description": "Hispasat es el operador español de satélites de comunicaciones, líder en la difusión y distribución de contenidos audiovisuales en español y portugués.",
    "description_en": "Hispasat is the Spanish communications satellite operator, a leader in the distribution of audiovisual content in Spanish and Portuguese.",
    "founded": 1989,
    "ceo": "Miguel Ángel Panduro",
    "sector": "Telecommunications",
    "tags": json.dumps(["Satellites", "Broadband", "Connectivity", "Telecommunications"]),
    "socialLinks": json.dumps({"twitter": "https://twitter.com/hispasat", "linkedin": "https://www.linkedin.com/company/hispasat"}),
    "keyPrograms": json.dumps(["Amazonas", "Hispasat", "AG1"]),
    "fundingStage": "Privately Held",
    "totalFunding": "N/A",
    "show": True
}

# Amazonas Nexus Data
amazonas_nexus_data = {
    "name": "Amazonas Nexus",
    "noradId": "55502",
    "purpose": "Communications (HTS)",
    "launchDate": date(2023, 2, 7),
    "orbitType": "GEO",
    "altitude": 35786.0,
    "inclination": 0.0,
    "description": "El Amazonas Nexus es un satélite de alto rendimiento (HTS) de nueva generación de Hispasat que proporciona conectividad de banda ancha en movilidad y servicios gubernamentales.",
    "description_en": "Amazonas Nexus is a next-generation High Throughput Satellite (HTS) from Hispasat providing broadband connectivity for mobility and government services.",
    "image": "/api/v1/satellite_images/amazonas-nexus.png",
    "isFeatured": True,
    "funFact": "Fue lanzado por un cohete Falcon 9 de SpaceX desde Cabo Cañaveral.",
    "funFact_en": "It was launched by a SpaceX Falcon 9 rocket from Cape Canaveral.",
    "show": True
}

def seed_database(name, url):
    print(f"\n--- Seeding {name} Database ---")
    try:
        engine = create_engine(url)
        Session = sessionmaker(bind=engine)
        session = Session()

        # 1. Handle Company (Hispasat)
        company_result = session.execute(text("SELECT id FROM companies WHERE name = 'Hispasat'")).fetchone()
        
        if company_result:
            print(f"  Hispasat already exists (ID: {company_result[0]}). Updating...")
            update_company = text("""
                UPDATE companies 
                SET type = :type, country = :country, "countryName" = :countryName, city = :city, 
                    coordinates = :coordinates, employees = :employees, website = :website, 
                    description = :description, description_en = :description_en, founded = :founded, 
                    ceo = :ceo, sector = :sector, tags = :tags, "socialLinks" = :socialLinks, 
                    "keyPrograms" = :keyPrograms, "fundingStage" = :fundingStage, 
                    "totalFunding" = :totalFunding, show = :show
                WHERE name = 'Hispasat'
            """)
            session.execute(update_company, hispasat_data)
            company_id = company_result[0]
        else:
            print("  Inserting Hispasat...")
            insert_company = text("""
                INSERT INTO companies (
                    name, type, country, "countryName", city, coordinates, employees, website, 
                    description, description_en, founded, ceo, sector, tags, "socialLinks", 
                    "keyPrograms", "fundingStage", "totalFunding", show
                ) VALUES (
                    :name, :type, :country, :countryName, :city, :coordinates, :employees, :website, 
                    :description, :description_en, :founded, :ceo, :sector, :tags, :socialLinks, 
                    :keyPrograms, :fundingStage, :totalFunding, :show
                ) RETURNING id
            """)
            company_id = session.execute(insert_company, hispasat_data).fetchone()[0]
        
        # 2. Handle Satellite (Amazonas Nexus)
        sat_result = session.execute(text("SELECT id FROM satellites WHERE name = 'Amazonas Nexus'")).fetchone()
        
        sat_data = {**amazonas_nexus_data, "operator_id": company_id}
        
        if sat_result:
            print(f"  Amazonas Nexus already exists. Updating...")
            update_sat = text("""
                UPDATE satellites 
                SET "noradId" = :noradId, operator_id = :operator_id, purpose = :purpose, 
                    "launchDate" = :launchDate, "orbitType" = :orbitType, altitude = :altitude, 
                    inclination = :inclination, description = :description, 
                    description_en = :description_en, image = :image, "isFeatured" = :isFeatured, 
                    "funFact" = :funFact, "funFact_en" = :funFact_en, show = :show
                WHERE name = 'Amazonas Nexus'
            """)
            session.execute(update_sat, sat_data)
        else:
            print("  Inserting Amazonas Nexus...")
            insert_sat = text("""
                INSERT INTO satellites (
                    name, "noradId", operator_id, purpose, "launchDate", "orbitType", 
                    altitude, inclination, description, description_en, image, 
                    "isFeatured", "funFact", "funFact_en", show
                ) VALUES (
                    :name, :noradId, :operator_id, :purpose, :launchDate, :orbitType, 
                    :altitude, :inclination, :description, :description_en, :image, 
                    :isFeatured, :funFact, :funFact_en, :show
                )
            """)
            session.execute(insert_sat, sat_data)
        
        session.commit()
        print(f"✅ SUCCESS: Seeded Amazonas Nexus and Hispasat in {name}!")
        session.close()
    except Exception as e:
        print(f"❌ ERROR seeding {name}: {e}")

if __name__ == "__main__":
    for db_name, db_url in db_urls:
        seed_database(db_name, db_url)
