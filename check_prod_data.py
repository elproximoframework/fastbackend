import sqlalchemy
from sqlalchemy import create_engine, text
import os

REMOTE_URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"

def check_production_data():
    print(f"Connecting to Remote DB...")
    try:
        engine = create_engine(REMOTE_URL)
        with engine.connect() as conn:
            # Check AppSetting
            result = conn.execute(text("SELECT key, value FROM app_settings WHERE key = 'featured_news_id'"))
            setting = result.fetchone()
            if setting:
                print(f"FOUND setting: {setting[0]} = {setting[1]}")
            else:
                print("MISSING setting: featured_news_id")

            # Check News count
            result = conn.execute(text("SELECT count(*) FROM news"))
            count = result.scalar()
            print(f"News count in production: {count}")

            if count > 0:
                result = conn.execute(text("SELECT id, title FROM news LIMIT 5"))
                for row in result:
                    print(f"News: ID={row[0]}, Title={row[1]}")

    except Exception as e:
        print(f"Error connecting to remote DB: {e}")

if __name__ == "__main__":
    check_production_data()
