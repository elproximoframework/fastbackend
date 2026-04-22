import sys
import os
from datetime import datetime, timedelta, timezone

# Add the parent directory to sys.path to import app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine
from app import models

def seed_challenges():
    models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Create Starship IFT-12 Challenge
        challenge_title = "Starship IFT-12: El Gran Salto"
        
        # Check if it already exists
        existing = db.query(models.Challenge).filter(models.Challenge.title == challenge_title).first()
        if existing:
            print(f"Challenge '{challenge_title}' already exists.")
            return

        # End date: Let's assume some future date for Starship IFT-12 (e.g., late 2026/27)
        # For now, let's set it to 6 months from now to keep it active
        end_date = datetime.now(timezone.utc) + timedelta(days=180)

        ift12_challenge = models.Challenge(
            title=challenge_title,
            title_en="Starship IFT-12: The Great Leap",
            description="¿Cuándo crees que despegará el decimosegundo vuelo de prueba de Starship? Participa y demuestra cuánto sabes del sector.",
            description_en="When do you think the twelfth Starship test flight will launch? Participate and show how much you know about the sector.",
            image_url="https://images.unsplash.com/photo-1517976487492-5750f3195933?q=80&w=2070&auto=format&fit=crop",
            end_date=end_date,
            is_active=True,
            type="date"
        )

        db.add(ift12_challenge)
        db.commit()
        print(f"Challenge '{challenge_title}' seeded successfully.")

    except Exception as e:
        print(f"Error seeding challenges: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_challenges()
