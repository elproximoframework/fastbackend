from app.database import engine
import sqlalchemy as sa

def list_companies():
    with engine.connect() as conn:
        result = conn.execute(sa.text("SELECT id, name, country FROM companies ORDER BY name"))
        for row in result:
            print(f"{row[0]}: {row[1]} ({row[2]})")

if __name__ == "__main__":
    list_companies()
