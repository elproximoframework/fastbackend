from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
import os
import sys

# Add current directory to path to import app.models
sys.path.append(os.getcwd())

from app.models import Company

DATABASE_URL = "postgresql://space_user:space_password@localhost:5433/space_db"
engine = create_engine(DATABASE_URL)

def get_unique_countries():
    with Session(engine) as session:
        query = select(Company.country).distinct()
        results = session.execute(query).scalars().all()
        # Also get country names if available, or just the codes
        query_detailed = select(Company.country, Company.countryName).distinct()
        detailed_results = session.execute(query_detailed).all()
        
        print("Unique Country Codes:")
        for country in sorted([c for c in results if c]):
            print(f"- {country}")
            
        print("\nCountry Mappings in DB:")
        for code, name in sorted(detailed_results, key=lambda x: str(x[0])):
            if code:
                print(f"- {code}: {name}")

if __name__ == "__main__":
    try:
        get_unique_countries()
    except Exception as e:
        print(f"Error: {e}")
