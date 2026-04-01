from sqlalchemy import create_engine, inspect
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://space_user:space_password@localhost:5433/space_db")
engine = create_engine(DATABASE_URL)
inspector = inspect(engine)

def check_table():
    columns = inspector.get_columns("spacex_inventory")
    print("Columns in spacex_inventory:")
    for column in columns:
        print(f"- {column['name']} ({column['type']})")

if __name__ == "__main__":
    try:
        check_table()
    except Exception as e:
        print(f"Error: {e}")
