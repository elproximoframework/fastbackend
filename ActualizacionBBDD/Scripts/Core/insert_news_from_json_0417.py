import json
import os
import sys

# Add backendfast to path to import app.models
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import News

LOCAL_DB_URL = "postgresql://space_user:space_password@localhost:5433/space_db"
REMOTE_DB_URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"

# Read JSON data
json_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '260417_noticias_index.json'))

with open(json_path, "r", encoding="utf-8") as f:
    news_data = json.load(f)

def insert_into_db(db_url, env_name):
    print(f"--- Connecting to {env_name} DB ---")
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    session = Session()

    for item in news_data:
        existing = session.query(News).filter(News.slug == item["slug"]).first()
        if existing:
            print(f"Updating existing record: {item['slug']}")
            for key, value in item.items():
                setattr(existing, key, value)
        else:
            print(f"Inserting new record: {item['slug']}")
            new_news = News(**item)
            session.add(new_news)
    
    session.commit()
    session.close()
    print(f"Finished {env_name} DB insert.\n")

if __name__ == "__main__":
    try:
        insert_into_db(LOCAL_DB_URL, "LOCAL")
    except Exception as e:
        print(f"Error in LOCAL: {e}")
        
    try:
        insert_into_db(REMOTE_DB_URL, "REMOTE")
    except Exception as e:
        print(f"Error in REMOTE: {e}")
