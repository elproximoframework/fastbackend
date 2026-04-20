from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Company
from app.database import engine

Session = sessionmaker(bind=engine)
session = Session()

def get_companies():
    try:
        last_companies = session.query(Company).order_by(Company.id.desc()).limit(20).all()
        for c in last_companies:
            print(f"ID: {c.id}, Name: {c.name}, Country: {c.country}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    get_companies()
