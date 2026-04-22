import sys
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Add root folder to sys.path to allow imports from app.models
sys.path.append(os.getcwd())

from app.models import Challenge, Prediction, Base

LOCAL_URL = "postgresql://space_user:space_password@localhost:5433/space_db"
REMOTE_URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"

def migrate():
    print("Starting migration...")
    
    local_engine = create_engine(LOCAL_URL)
    remote_engine = create_engine(REMOTE_URL)
    
    # Create tables on remote if they don't exist
    print("Creating tables on remote...")
    # We only want to create Challenges and Predictions to avoid interfering with other tables
    Challenge.__table__.create(remote_engine, checkfirst=True)
    Prediction.__table__.create(remote_engine, checkfirst=True)
    
    LocalSession = sessionmaker(bind=local_engine)
    RemoteSession = sessionmaker(bind=remote_engine)
    
    local_session = LocalSession()
    remote_session = RemoteSession()
    
    try:
        # 1. Migrate Challenges
        print("Migrating challenges...")
        local_challenges = local_session.query(Challenge).all()
        for ch in local_challenges:
            # Check if exists
            exists = remote_session.query(Challenge).filter_by(id=ch.id).first()
            if not exists:
                # Create a new instance to avoid session attachment issues
                new_ch = Challenge(
                    id=ch.id,
                    title=ch.title,
                    title_en=ch.title_en,
                    description=ch.description,
                    description_en=ch.description_en,
                    image_url=ch.image_url,
                    end_date=ch.end_date,
                    prediction_deadline=ch.prediction_deadline,
                    actual_event_date=ch.actual_event_date,
                    is_active=ch.is_active,
                    prize_description=ch.prize_description,
                    prize_description_en=ch.prize_description_en,
                    prize_image_url=ch.prize_image_url,
                    type=ch.type,
                    options=ch.options,
                    created_at=ch.created_at
                )
                remote_session.add(new_ch)
        
        remote_session.commit()
        print(f"Migrated {len(local_challenges)} challenges.")
        
        # 2. Migrate Predictions
        print("Migrating predictions...")
        local_predictions = local_session.query(Prediction).all()
        for p in local_predictions:
            exists = remote_session.query(Prediction).filter_by(id=p.id).first()
            if not exists:
                new_p = Prediction(
                    id=p.id,
                    challenge_id=p.challenge_id,
                    nickname=p.nickname,
                    email=p.email,
                    prediction_value=p.prediction_value,
                    verification_code=p.verification_code,
                    created_at=p.created_at
                )
                remote_session.add(new_p)
                
        remote_session.commit()
        print(f"Migrated {len(local_predictions)} predictions.")
        
        # 3. Reset sequences
        print("Resetting sequences...")
        with remote_engine.connect() as conn:
            conn.execute(text("SELECT setval('challenges_id_seq', (SELECT MAX(id) FROM challenges))"))
            conn.execute(text("SELECT setval('predictions_id_seq', (SELECT MAX(id) FROM predictions))"))
            conn.commit()
        print("Sequences reset successfully.")
        
        print("Migration completed successfully!")
        
    except Exception as e:
        print(f"Error during migration: {e}")
        remote_session.rollback()
    finally:
        local_session.close()
        remote_session.close()

if __name__ == "__main__":
    migrate()
