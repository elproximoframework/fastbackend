from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Company
from app.database import engine
import os

Session = sessionmaker(bind=engine)
session = Session()

def get_companies():
    try:
        # Check IDs 101 to 105
        ids = range(101, 106)
        companies = session.query(Company).filter(Company.id.in_(ids)).all()
        
        if not companies:
            print("No companies found for IDs 101-105. Checking if they exist under different IDs or listing the last 10 companies.")
            last_companies = session.query(Company).order_by(Company.id.desc()).limit(10).all()
            for c in last_companies:
                print(f"ID: {c.id}, Name: {c.name}, Country: {c.country}")
        else:
            for c in companies:
                print(f"ID: {c.id}, Name: {c.name}, Country: {c.country}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    get_companies()
