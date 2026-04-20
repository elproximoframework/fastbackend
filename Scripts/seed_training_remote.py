import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add the parent directory to sys.path to import app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import models

# Remote URL provided by user
REMOTE_URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"

def seed_training_remote():
    # Create engine for remote DB
    engine = create_engine(REMOTE_URL)
    SessionRemote = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionRemote()
    
    try:
        print(f"Connecting to remote database...")
        # Create table if it doesn't exist on remote
        models.Base.metadata.create_all(bind=engine)
        
        # Check if already seeded
        if db.query(models.Training).count() > 0:
            print("Remote Training table already contains data. Skipping seeding.")
            return

        training_data = [
            {
                "slug": "upm-universidad-politecnica-madrid",
                "name": "Universidad Politécnica de Madrid (UPM)",
                "name_en": "Polytechnic University of Madrid (UPM)",
                "type": "university",
                "name_file": "upm.md",
                "description": "Líder en ingeniería aeroespacial en España, con una larga tradición y fuertes vínculos con la industria.",
                "description_en": "Leader in aerospace engineering in Spain, with a long tradition and strong industrial ties.",
                "link": "https://www.upm.es/",
                "show": True
            },
            {
                "slug": "master-ciencia-tecnologia-espacial-upm",
                "name": "Máster Universitario en Ciencia y Tecnología Espacial",
                "name_en": "Master in Space Science and Technology",
                "type": "master",
                "name_file": "master-espacial-upm.md",
                "description": "Programa especializado en los fundamentos científicos y técnicos del espacio, impartido por la UPM.",
                "description_en": "Specialized program in the scientific and technical foundations of space, taught by UPM.",
                "link": None,
                "show": True
            },
            {
                "slug": "grado-ingenieria-aeroespacial",
                "name": "Grado en Ingeniería Aeroespacial",
                "name_en": "Bachelor's Degree in Aerospace Engineering",
                "type": "grade",
                "name_file": "grado-aeroespacial.md",
                "description": "Formación integral en el diseño, desarrollo y gestión de vehículos aeroespaciales.",
                "description_en": "Comprehensive training in the design, development, and management of aerospace vehicles.",
                "link": None,
                "show": True
            },
            {
                "slug": "universidad-sevilla",
                "name": "Universidad de Sevilla",
                "name_en": "University of Seville",
                "type": "university",
                "name_file": "us.md",
                "description": "Destacada por su centro de ingeniería y colaboración con el clúster aeroespacial andaluz.",
                "description_en": "Notable for its engineering center and collaboration with the Andalusian aerospace cluster.",
                "link": "https://www.us.es/",
                "show": True
            },
            {
                "slug": "doctorado-ingenieria-aeroespacial",
                "name": "Programa de Doctorado en Ingeniería Aeroespacial",
                "name_en": "PhD Program in Aerospace Engineering",
                "type": "phd",
                "name_file": "phd-aero.md",
                "description": "Investigación avanzada en propulsión, estructuras y sistemas espaciales.",
                "description_en": "Advanced research in propulsion, structures, and space systems.",
                "link": None,
                "show": True
            }
        ]

        print(f"Seeding {len(training_data)} records...")
        for item_data in training_data:
            item = models.Training(**item_data)
            db.add(item)
        
        db.commit()
        print(f"Successfully seeded remote training records.")
        
    except Exception as e:
        print(f"Error seeding remote data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_training_remote()
