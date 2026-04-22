import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))

def set_test_deadline():
    with engine.connect() as conn:
        # Set deadline to 1 day ago
        past_date = datetime.now(timezone.utc) - timedelta(days=1)
        conn.execute(text("UPDATE challenges SET prediction_deadline = :deadline WHERE id = 1"), {"deadline": past_date})
        conn.commit()
        print(f"Deadline for challenge 1 set to {past_date}")

if __name__ == "__main__":
    set_test_deadline()
