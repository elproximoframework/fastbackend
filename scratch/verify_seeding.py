
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
import os

LOCAL_URL = "postgresql://space_user:space_password@localhost:5433/space_db"

def verify_seeding():
    engine = sa.create_engine(LOCAL_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    new_slugs = [
        "ercx-space", "labpadre", "thespacexfans", "alpha-tech", 
        "spaceflight-now", "tech-map", "great-spacex", "the-space-community",
        "video-from-space", "space-affairs", "rgv-aerial-photography",
        "astronauta-lili", "spacexstorm", "explorando-el-espacio"
    ]
    
    print(f"Checking for {len(new_slugs)} new slugs in local database...")
    
    try:
        with engine.connect() as connection:
            result = connection.execute(sa.text("SELECT slug FROM media_sources WHERE slug IN :slugs"), {"slugs": tuple(new_slugs)})
            found_slugs = [row[0] for row in result]
        
        print(f"Found {len(found_slugs)} out of {len(new_slugs)} slugs.")
        for slug in new_slugs:
            if slug in found_slugs:
                print(f"  [X] {slug}")
            else:
                print(f"  [ ] {slug} (NOT FOUND)")
                
    except Exception as e:
        print(f"Error querying database: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    verify_seeding()
