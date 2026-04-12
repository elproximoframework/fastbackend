from app.database import SessionLocal
from app.models import Company
from app.schemas import CompanyResponse
from pydantic import ValidationError

def debug_companies():
    db = SessionLocal()
    try:
        companies = db.query(Company).filter(Company.show == True).all()
        print(f"Checking {len(companies)} companies...")
        
        errors = []
        for c in companies:
            try:
                CompanyResponse.model_validate(c)
            except ValidationError as e:
                errors.append((c.id, c.name, e))
        
        print(f"Found {len(errors)} companies with validation errors.")
        for cid, name, err in errors:
            print(f"\nID={cid}, Name={name}")
            print(f"Error: {err}")
            
    finally:
        db.close()

if __name__ == "__main__":
    debug_companies()
