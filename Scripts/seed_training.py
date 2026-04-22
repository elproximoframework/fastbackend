import sys
import os

# Add the parent directory to sys.path to import app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import models

# Database Configuration
REMOTE_URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"
LOCAL_URL = "postgresql://space_user:space_password@localhost:5433/space_db"

def seed_db(db_url, label):
    print(f"\n--- Seeding {label} Training Database ---")
    
    # Set environment variable because app.database expects it
    os.environ["DATABASE_URL"] = db_url
    
    # Create engine for target DB
    try:
        engine = create_engine(db_url)
        Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = Session()
        
        print(f"Connecting to {label} database...")
        # Create table if it doesn't exist
        models.Base.metadata.create_all(bind=engine)
        
        # Get existing slugs to avoid duplicates
        existing_slugs = [s[0] for s in db.query(models.Training.slug).all()]

        """
        CAMPOS DE TRAINING:
        - slug: Identificador único (URL friendly).
        - name: Nombre de la institución o programa (ES).
        - name_en: Nombre de la institución o programa (EN).
        - type: Tipo de formación. 
            Valores: 'grade', 'master', 'phd', 'university'
        - name_file: Nombre del archivo Markdown asociado (contenido detallado).
        - description: Resumen breve en español.
        - description_en: Resumen breve en inglés.
        - link: Enlace externo (web oficial).
        - show: Flag de visibilidad en la plataforma.
        """
        training_data = [
{
    "slug": "phd-aeronautics-astronautics-mit",
    "name": "Doctorado en Aeronáutica y Astronáutica - MIT",
    "name_en": "Ph.D. in Aeronautics and Astronautics - MIT",
    "type": "phd",
    "name_file": None,
    "description": "Programa líder mundial que desarrolla tecnologías pioneras para la exploración espacial, sistemas autónomos y propulsión avanzada en constante colaboración con la NASA.",
    "description_en": "World-leading program developing pioneering technologies for space exploration, autonomous systems, and advanced propulsion in constant collaboration with NASA.",
    "link": "https://aeroastro.mit.edu/graduate-program/doctoral-program/",
    "show": True
  },
  {
    "slug": "phd-space-engineering-caltech",
    "name": "Doctorado en Ingeniería Espacial - Caltech",
    "name_en": "Ph.D. in Space Engineering - Caltech",
    "type": "phd",
    "name_file": None,
    "description": "Integrado en el prestigioso laboratorio GALCIT y fuertemente conectado al JPL de la NASA, es referencia mundial en mecánica de fluidos, sólidos y propulsión espacial.",
    "description_en": "Integrated into the prestigious GALCIT laboratory and heavily connected to NASA's JPL, it is a world reference in fluid mechanics, solids, and space propulsion.",
    "link": "https://galcit.caltech.edu/academics/degrees/phd",
    "show": True
  },
  {
    "slug": "phd-aeronautics-astronautics-stanford",
    "name": "Doctorado en Aeronáutica y Astronáutica - Stanford",
    "name_en": "Ph.D. in Aeronautics and Astronautics - Stanford University",
    "type": "phd",
    "name_file": None,
    "description": "Orientado a la investigación profunda en robótica espacial, astrodinámica y diseño de satélites, con una enorme influencia directa en la industria del New Space en Silicon Valley.",
    "description_en": "Oriented towards deep research in space robotics, astrodynamics, and satellite design, with enormous direct influence on the New Space industry in Silicon Valley.",
    "link": "https://aeroastro.stanford.edu/academics/graduate-program",
    "show": True
  },
  {
    "slug": "phd-aerospace-engineering-cuboulder",
    "name": "Doctorado en Ciencias de la Ingeniería Aeroespacial - CU Boulder",
    "name_en": "Ph.D. in Aerospace Engineering Sciences - CU Boulder",
    "type": "phd",
    "name_file": None,
    "description": "Reconocido por su investigación en astrodinámica, teledetección satelital y bioastronáutica. Es una de las universidades públicas que más fondos recibe de la NASA.",
    "description_en": "Recognized for its research in astrodynamics, satellite remote sensing, and bioastronautics. It is one of the top public universities receiving NASA funding.",
    "link": "https://www.colorado.edu/aerospace/academics/graduate",
    "show": True
  },
  {
    "slug": "phd-astronautical-engineering-usc",
    "name": "Doctorado en Ingeniería Astronáutica - USC",
    "name_en": "Ph.D. in Astronautical Engineering - University of Southern California",
    "type": "phd",
    "name_file": None,
    "description": "Uno de los escasos programas puramente dedicados al espacio (sin la parte de aviación), especializado de lleno en dinámica orbital, propulsión y operaciones espaciales.",
    "description_en": "One of the rare programs purely dedicated to space (without the aviation part), fully specialized in orbital dynamics, propulsion, and space operations.",
    "link": "https://viterbigradadmission.usc.edu/programs/doctoral/astronautical-engineering/",
    "show": True
  },
  {
    "slug": "phd-aeronautics-astronautics-purdue",
    "name": "Doctorado en Aeronáutica y Astronáutica - Purdue University",
    "name_en": "Ph.D. in Aeronautics and Astronautics - Purdue University",
    "type": "phd",
    "name_file": None,
    "description": "Conocida como la 'Cuna de Astronautas', ofrece un doctorado altamente centrado en el desarrollo integral de vehículos espaciales, estructuras y diseño de misiones.",
    "description_en": "Known as the 'Cradle of Astronauts', it offers a Ph.D. highly focused on the comprehensive development of spacecraft, structures, and mission design.",
    "link": "https://engineering.purdue.edu/AAE/academics/graduate/phd",
    "show": True
  },
  {
    "slug": "phd-aerospace-engineering-georgiatech",
    "name": "Doctorado en Ingeniería Aeroespacial - Georgia Tech",
    "name_en": "Ph.D. in Aerospace Engineering - Georgia Tech",
    "type": "phd",
    "name_file": None,
    "description": "Programa de excelencia académica con una potente división dedicada a la ingeniería de sistemas espaciales, propulsores eléctricos y arquitectura de misiones planetarias.",
    "description_en": "Program of academic excellence with a powerful division dedicated to space systems engineering, electric thrusters, and planetary mission architecture.",
    "link": "https://ae.gatech.edu/academics/graduate/phd",
    "show": True
  },
  {
    "slug": "phd-aerospace-engineering-umich",
    "name": "Doctorado en Ingeniería Aeroespacial - University of Michigan",
    "name_en": "Ph.D. in Aerospace Engineering - University of Michigan",
    "type": "phd",
    "name_file": None,
    "description": "Destaca mundialmente por su Laboratorio de Propulsión de Plasmadinámica (PEPL) y la investigación en sistemas de exploración espacial profunda.",
    "description_en": "Stands out worldwide for its Plasmadynamics and Electric Propulsion Laboratory (PEPL) and research in deep space exploration systems.",
    "link": "https://aero.engin.umich.edu/academics/grad/phd-program/",
    "show": True
  },
  {
    "slug": "phd-aerospace-engineering-utaustin",
    "name": "Doctorado en Ingeniería Aeroespacial - UT Austin",
    "name_en": "Ph.D. in Aerospace Engineering - University of Texas at Austin",
    "type": "phd",
    "name_file": None,
    "description": "Famoso por su centro de investigación en mecánica orbital e ingeniería de vehículos espaciales, vital para el seguimiento de satélites y la limpieza de basura espacial.",
    "description_en": "Famous for its research center in orbital mechanics and spacecraft engineering, vital for satellite tracking and space debris cleanup.",
    "link": "https://www.ae.utexas.edu/academics/graduate/phd-program",
    "show": True
  },
  {
    "slug": "phd-planetary-sciences-ucf",
    "name": "Doctorado en Ciencias Planetarias - UCF",
    "name_en": "Ph.D. in Planetary Sciences - University of Central Florida",
    "type": "phd",
    "name_file": None,
    "description": "Estratégicamente ubicado cerca del Centro Espacial Kennedy de la NASA, este doctorado investiga exoplanetas, superficies lunares/marcianas y minería de asteroides.",
    "description_en": "Strategically located near NASA's Kennedy Space Center, this Ph.D. investigates exoplanets, lunar/Martian surfaces, and asteroid mining.",
    "link": "https://planets.ucf.edu/academics/phd-in-planetary-sciences/",
    "show": True
  }
]

        added_count = 0
        updated_count = 0
        
        for item_data in training_data:
            if item_data["slug"] in existing_slugs:
                # Update existing record
                db.query(models.Training).filter(models.Training.slug == item_data["slug"]).update(item_data)
                updated_count += 1
            else:
                # Add new record
                item = models.Training(**item_data)
                db.add(item)
                added_count += 1
        
        db.commit()
        print(f"Success! {added_count} records added, {updated_count} records updated.")
        db.close()
        
    except Exception as e:
        print(f"Error seeding {label} training database: {e}")

if __name__ == "__main__":
    # Seed Local DB
    seed_db(LOCAL_URL, "LOCAL")
    
    # Seed Remote DB
    seed_db(REMOTE_URL, "REMOTE")
