from pydantic import ValidationError
from app.models import SpaceXInventory
from app.schemas import SpaceXInventoryResponse
from app.database import SessionLocal
import json

def test_validation():
    db = SessionLocal()
    try:
        items = db.query(SpaceXInventory).all()
        print(f"Total items in DB: {len(items)}")
        for item in items:
            try:
                # Convert SQLAlchemy model to Pydantic
                p_item = SpaceXInventoryResponse.from_orm(item)
            except ValidationError as e:
                print(f"\nValidation error for ID {item.id} ({item.title}):")
                for err in e.errors():
                    print(f"  Field: {err['loc']}, Error: {err['msg']}, Type: {err['type']}")
            except Exception as e:
                print(f"\nOther error for ID {item.id}: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    test_validation()
