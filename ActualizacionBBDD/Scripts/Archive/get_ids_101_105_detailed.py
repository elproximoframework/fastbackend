from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Company
from app.database import engine

Session = sessionmaker(bind=engine)
session = Session()

def get_companies():
    try:
        ids = [101, 102, 103, 104, 105]
        companies = session.query(Company).filter(Company.id.in_(ids)).all()
        found_ids = {c.id for c in companies}
        for c in companies:
            print(f"ID: {c.id}, Name: {c.name}, Country: {c.country}")
        for i in ids:
            if i not in found_ids:
                print(f"ID: {i} NOT FOUND")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    get_companies()
