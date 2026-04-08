from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Company
from app.database import engine

Session = sessionmaker(bind=engine)
session = Session()

def get_companies():
    try:
        ids = [101, 102, 103, 104, 105]
        companies = session.query(Company).filter(Company.id.in_(ids)).order_by(Company.id).all()
        for c in companies:
            print(f"ID: {c.id}, Name: {c.name}, Country: {c.country}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    get_companies()
