import sys
import os
import re

# Add the backendfast directory to the Python path so 'app' can be imported easily
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from sqlalchemy import text, create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Company

def slugify(text_val):
    if not text_val:
        return "unknown"
    t = text_val.lower()
    t = re.sub(r'[^a-z0-9]+', '-', t)
    return t.strip('-')

def update_companies_schema():
    print("Connecting to REMOTE PostgreSQL database...")
    
    # Use remote URL directly
    REMOTE_URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"
    engine = create_engine(REMOTE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    with engine.connect() as conn:
        try:
            # Check if slug exists
            result = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name='companies' AND column_name='slug';"))
            if not result.fetchone():
                print("Adding 'slug' column to 'companies' table...")
                conn.execute(text("ALTER TABLE companies ADD COLUMN slug VARCHAR;"))
            else:
                print("'slug' column already exists.")

            # Check if rutainformacion exists
            result = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name='companies' AND column_name='rutainformacion';"))
            if not result.fetchone():
                print("Adding 'rutainformacion' column to 'companies' table...")
                conn.execute(text("ALTER TABLE companies ADD COLUMN rutainformacion VARCHAR;"))
            else:
                print("'rutainformacion' column already exists.")
            
            # Add index if it doesn't exist
            result = conn.execute(text("SELECT indexname FROM pg_indexes WHERE tablename='companies' AND indexname='ix_companies_slug';"))
            if not result.fetchone():
                conn.execute(text("CREATE UNIQUE INDEX ix_companies_slug ON companies(slug);"))
                print("Created unique index 'ix_companies_slug'.")

            conn.commit()
            print("Schema updated successfully on remote DB.")

        except Exception as e:
            print(f"Database schema error: {e}")
            conn.rollback()
            pass

    # Update data using ORM session to generate slugs
    db = SessionLocal()
    try:
        companies = db.query(Company).filter((Company.slug == None) | (Company.slug == '')).all()
        for company in companies:
            base_slug = slugify(company.name)
            slug = base_slug
            
            # ensure uniqueness
            exists = db.query(Company).filter(Company.slug == slug, Company.id != company.id).first()
            if exists:
                slug = f"{base_slug}-{company.id}"
                
            company.slug = slug
            print(f"Updated REMOTE company ID {company.id} ('{company.name}') -> slug: {slug}")
            
        # Add a dummy record for SpaceX to test functionality if needed
        spacex_company = db.query(Company).filter(Company.name.ilike('spacex')).first()
        if spacex_company and not spacex_company.rutainformacion:
            spacex_company.rutainformacion = 'spacex_report.md'
            print("Se ha configurado 'spacex_report.md' como rutainformacion para SpaceX remoto por defecto.")
            
        if companies or spacex_company:
            db.commit()
            print("Remote data explicitly updated with slugs and dummy test report.")
        else:
            print("All remote companies already have slugs.")
            
    except Exception as e:
        print(f"Data update error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    update_companies_schema()
