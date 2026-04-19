from sqlalchemy import create_engine, inspect, text
import os

DATABASE_URL = "postgresql://space_user:space_password@localhost:5433/space_db"
engine = create_engine(DATABASE_URL)

def verify():
    with engine.connect() as conn:
        # Check schema
        inspector = inspect(engine)
        columns = inspector.get_columns("companies")
        has_col = any(c['name'] == 'company_validated' for c in columns)
        print(f"Column 'company_validated' exists: {has_col}")
        
        # Check data for SpaceX
        result = conn.execute(text("SELECT name, validated, company_validated FROM companies WHERE name ILIKE '%SpaceX%' LIMIT 1"))
        row = result.fetchone()
        if row:
            print(f"Company: {row[0]}")
            print(f"  validated (Resp): {row[1]}")
            print(f"  company_validated (Emp): {row[2]}")
        else:
            print("SpaceX not found in DB")

if __name__ == "__main__":
    verify()
