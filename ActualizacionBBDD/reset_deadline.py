import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))

def reset_deadline():
    with engine.connect() as conn:
        conn.execute(text("UPDATE challenges SET prediction_deadline = NULL WHERE id = 1"))
        conn.commit()
        print("Deadline for challenge 1 reset to NULL")

if __name__ == "__main__":
    reset_deadline()
