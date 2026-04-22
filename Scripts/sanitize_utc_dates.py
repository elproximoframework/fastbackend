import sys
import os
from datetime import datetime, timezone

# Add the parent directory to sys.path to import app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app import models

def sanitize_dates():
    db = SessionLocal()
    try:
        challenges = db.query(models.Challenge).all()
        for challenge in challenges:
            updated = False
            # Check end_date
            if challenge.end_date and challenge.end_date.tzinfo is None:
                challenge.end_date = challenge.end_date.replace(tzinfo=timezone.utc)
                updated = True
                
            # Check prediction_deadline
            if challenge.prediction_deadline and challenge.prediction_deadline.tzinfo is None:
                challenge.prediction_deadline = challenge.prediction_deadline.replace(tzinfo=timezone.utc)
                updated = True
            
            if updated:
                print(f"Updated challenge {challenge.id} ({challenge.title}) to UTC")
        
        db.commit()
        print("Sanitization complete.")
    except Exception as e:
        print(f"Error during sanitization: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    sanitize_dates()
