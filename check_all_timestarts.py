from app.models import SpaceXInventory
from app.database import SessionLocal
import reprlib

def check_all_timestarts():
    db = SessionLocal()
    try:
        items = db.query(SpaceXInventory).all()
        for item in items:
            print(f"ID: {item.id}, Title: {item.title}, timestart: {repr(item.timestart)}, type: {type(item.timestart)}")
    finally:
        db.close()

if __name__ == "__main__":
    check_all_timestarts()
