from pydantic import ValidationError
from app.models import Company
from app.schemas import CompanyResponse
from app.database import SessionLocal
import json

def test_validation():
    db = SessionLocal()
    try:
        companies = db.query(Company).filter(Company.show == True).all()
        print(f"Total companies in DB (show=True): {len(companies)}")
        errors_found = 0
        for company in companies:
            try:
                # Convert SQLAlchemy model to Pydantic
                p_company = CompanyResponse.model_validate(company)
            except ValidationError as e:
                errors_found += 1
                print(f"\nValidation error for ID {company.id} ({company.name}):")
                for err in e.errors():
                    print(f"  Field: {err['loc']}, Error: {err['msg']}, Type: {err['type']}")
                print(f"  Full company data: {json.dumps({c.name: getattr(company, c.name) for c in company.__table__.columns if not isinstance(getattr(company, c.name), (bytes,))}, indent=2, default=str)}")
            except Exception as e:
                errors_found += 1
                print(f"\nOther error for ID {company.id}: {e}")
        
        if errors_found == 0:
            print("\nNo validation errors found in companies table.")
    finally:
        db.close()

if __name__ == "__main__":
    test_validation()
