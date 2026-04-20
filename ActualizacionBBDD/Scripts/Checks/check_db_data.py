from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from app.models import SpaceXInventory
from app.database import engine
import os

Session = sessionmaker(bind=engine)
session = Session()

def check_data():
    try:
        items = session.query(SpaceXInventory).limit(10).all()
        print(f"Found {len(items)} items.")
        for item in items:
            print(f"ID: {item.id}, Title: {item.title}, Date: {item.date}")
    except Exception as e:
        print(f"Error querying data: {e}")

if __name__ == "__main__":
    check_data()
