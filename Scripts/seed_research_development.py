import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timezone

# Add the parent directory to sys.path to import app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import models

# Database Configuration
REMOTE_URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"
LOCAL_URL = "postgresql://space_user:space_password@localhost:5433/space_db"

def seed_db(db_url, label):
    print(f"\n--- Seeding {label} Database ---")
    
    # Set environment variable because app.database expects it
    os.environ["DATABASE_URL"] = db_url
    
    # Import models here to ensure the env var is picked up if needed
    from app import models
    
    # Create engine for target DB
    try:
        engine = create_engine(db_url)
        Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = Session()
        
        print(f"Connecting to {label} database...")
        # Create table if it doesn't exist
        models.Base.metadata.create_all(bind=engine)
        
        # Get existing slugs to avoid duplicates
        existing_slugs = [s[0] for s in db.query(models.ResearchDevelopment.slug).all()]

        """
        CAMPOS DE RESEARCHDEVELOPMENT (I+D):
        - slug: Identificador único (URL friendly). Obligatorio.
        - name: Nombre en español. Obligatorio.
        - name_en: Nombre en inglés.
        - type: Categoría del recurso. Obligatorio.
            Valores válidos: 'researchcenter', 'researchmagazine', 'paper', 'conference', 'estateoftheart'
        - description: Resumen en español.
        - description_en: Resumen en inglés.
        - link: Enlace externo (web oficial, PDF, etc).
        - file: Nombre del archivo Markdown local asociado (ej: 'starship-propulsion.md').
        - show: Booleano para visibilidad (default: True).
        """
        research_data = [
{
    "slug": "mit-aeroastro",
    "name": "Massachusetts Institute of Technology (MIT) - Departamento de Aeronáutica y Astronáutica",
    "name_en": "Massachusetts Institute of Technology (MIT) - Department of Aeronautics and Astronautics (AeroAstro)",
    "type": "university",
    "name_file": None,
    "description": "Considerado el mejor programa aeroespacial del mundo, pionero en la exploración espacial, robótica orbital y sistemas astronáuticos.",
    "description_en": "Considered the best aerospace program in the world, a pioneer in space exploration, orbital robotics, and astronautical systems.",
    "link": "https://aeroastro.mit.edu/",
    "show": True
  },
  {
    "slug": "caltech-galcit",
    "name": "California Institute of Technology (Caltech) - GALCIT",
    "name_en": "California Institute of Technology (Caltech) - Graduate Aerospace Laboratories (GALCIT)",
    "type": "university",
    "name_file": None,
    "description": "Centro histórico en la investigación espacial, estrechamente vinculado al JPL de la NASA, líder en propulsión y mecánica de fluidos.",
    "description_en": "Historic center in space research, closely tied to NASA's JPL, leading in propulsion and fluid mechanics.",
    "link": "https://galcit.caltech.edu/",
    "show": True
  },
  {
    "slug": "stanford-aeroastro",
    "name": "Universidad de Stanford - Departamento de Aeronáutica y Astronáutica",
    "name_en": "Stanford University - Department of Aeronautics and Astronautics",
    "type": "university",
    "name_file": None,
    "description": "Ubicado en Silicon Valley, destaca en sistemas espaciales autónomos, New Space, GPS y control de satélites.",
    "description_en": "Located in Silicon Valley, it excels in autonomous space systems, New Space, GPS, and satellite control.",
    "link": "https://aeroastro.stanford.edu/",
    "show": True
  },
  {
    "slug": "tudelft-aerospace",
    "name": "Universidad Tecnológica de Delft (TU Delft) - Facultad de Ingeniería Aeroespacial",
    "name_en": "Delft University of Technology (TU Delft) - Faculty of Aerospace Engineering",
    "type": "university",
    "name_file": None,
    "description": "Una de las facultades aeroespaciales más grandes de Europa, referente mundial en miniaturización de satélites e innovación espacial.",
    "description_en": "One of the largest aerospace faculties in Europe, a global benchmark in satellite miniaturization and space innovation.",
    "link": "https://www.tudelft.nl/en/ae",
    "show": True
  },
  {
    "slug": "isae-supaero",
    "name": "ISAE-SUPAERO (Instituto Superior de Aeronáutica y del Espacio)",
    "name_en": "ISAE-SUPAERO (Higher Institute of Aeronautics and Space)",
    "type": "university",
    "name_file": "",
    "description": "Institución francesa líder en Europa, fundamental para la Agencia Espacial Europea (ESA) y la industria aeroespacial de Toulouse.",
    "description_en": "Leading French institution in Europe, fundamental to the European Space Agency (ESA) and the Toulouse aerospace industry.",
    "link": "https://www.isae-supaero.fr/",
    "show": True
  },
  {
    "slug": "purdue-aae",
    "name": "Universidad Purdue - Escuela de Aeronáutica y Astronáutica",
    "name_en": "Purdue University - School of Aeronautics and Astronautics",
    "type": "university",
    "name_file": None,
    "description": "Conocida como la 'Cuna de Astronautas', tiene uno de los programas de ingeniería espacial y diseño de misiones más prestigiosos de EE. UU.",
    "description_en": "Known as the 'Cradle of Astronauts', it has one of the most prestigious space engineering and mission design programs in the US.",
    "link": "https://engineering.purdue.edu/AAE",
    "show": True
  },
  {
    "slug": "georgiatech-ae",
    "name": "Georgia Tech - Escuela Daniel Guggenheim de Ingeniería Aeroespacial",
    "name_en": "Georgia Tech - Daniel Guggenheim School of Aerospace Engineering",
    "type": "university",
    "name_file": None,
    "description": "Ofrece uno de los programas aeroespaciales más grandes e intensivos en investigación del mundo, con gran peso en sistemas espaciales.",
    "description_en": "Offers one of the largest and most research-intensive aerospace programs globally, with a strong emphasis on space systems.",
    "link": "https://ae.gatech.edu/",
    "show": True
  },
  {
    "slug": "cuboulder-aerospace",
    "name": "Universidad de Colorado Boulder - Ingeniería Aeroespacial",
    "name_en": "University of Colorado Boulder - Aerospace Engineering Sciences",
    "type": "university",
    "name_file": None,
    "description": "Centro vital para la NASA y operaciones espaciales civiles y militares, destacando en ciencias atmosféricas y misiones planetarias.",
    "description_en": "Vital center for NASA and civil/military space operations, excelling in atmospheric sciences and planetary missions.",
    "link": "https://www.colorado.edu/aerospace/",
    "show": True
  },
  {
    "slug": "imperial-college-aeronautics",
    "name": "Imperial College London - Departamento de Aeronáutica",
    "name_en": "Imperial College London - Department of Aeronautics",
    "type": "university",
    "name_file": None,
    "description": "Líder en el Reino Unido, reconocido por su investigación de vanguardia en aerodinámica, estructuras aeroespaciales y misiones.",
    "description_en": "Leader in the UK, renowned for its cutting-edge research in aerodynamics, aerospace structures, and missions.",
    "link": "https://www.imperial.ac.uk/aeronautics/",
    "show": True
  },
  {
    "slug": "polimi-daer",
    "name": "Politécnico de Milán - Departamento de Ciencia y Tecnología Aeroespacial",
    "name_en": "Politecnico di Milano - Department of Aerospace Science and Technology (DAER)",
    "type": "university",
    "name_file": None,
    "description": "La principal universidad aeroespacial de Italia, clave en misiones europeas de exploración espacial y dinámica de vuelo.",
    "description_en": "Italy's premier aerospace university, key in European space exploration missions and flight dynamics.",
    "link": "https://www.aero.polimi.it/",
    "show": True
  },
  {
    "slug": "eth-zurich-space",
    "name": "ETH Zurich - Instituto de Sistemas Espaciales",
    "name_en": "ETH Zurich - Space Systems",
    "type": "university",
    "name_file": None,
    "description": "Universidad suiza de élite mundial con un fuerte enfoque en robótica espacial, astrofísica y desarrollo de instrumentos orbitales.",
    "description_en": "World-elite Swiss university with a strong focus on space robotics, astrophysics, and orbital instrument development.",
    "link": "https://space.ethz.ch/",
    "show": True
  },
  {
    "slug": "tum-aerospace",
    "name": "Universidad Técnica de Múnich (TUM) - Aeroespacial y Geodesia",
    "name_en": "Technical University of Munich (TUM) - Department of Aerospace and Geodesy",
    "type": "university",
    "name_file": None,
    "description": "Potencia aeroespacial en Alemania, centrada en la intersección de la navegación por satélite, observación de la Tierra y tecnología espacial.",
    "description_en": "Aerospace powerhouse in Germany, focused on the intersection of satellite navigation, Earth observation, and space tech.",
    "link": "https://www.asg.ed.tum.de/",
    "show": True
  },
  {
    "slug": "cranfield-aerospace",
    "name": "Universidad de Cranfield - Escuela Aeroespacial",
    "name_en": "Cranfield University - Aerospace",
    "type": "university",
    "name_file": None,
    "description": "Universidad de posgrado británica, famosa por tener su propio aeropuerto e instalaciones de investigación espacial aplicada a la industria.",
    "description_en": "British postgraduate university famous for having its own airport and applied space research facilities tied to industry.",
    "link": "https://www.cranfield.ac.uk/aerospace",
    "show": True
  },
  {
    "slug": "umich-aerospace",
    "name": "Universidad de Michigan - Ingeniería Aeroespacial",
    "name_en": "University of Michigan - Aerospace Engineering",
    "type": "university",
    "name_file": None,
    "description": "Uno de los programas aeroespaciales más antiguos y prestigiosos, con una profunda historia en el programa Apolo y misiones modernas.",
    "description_en": "One of the oldest and most prestigious aerospace programs, with deep history in the Apollo program and modern missions.",
    "link": "https://aero.engin.umich.edu/",
    "show": True
  },
  {
    "slug": "utias-toronto",
    "name": "Instituto de Estudios Aeroespaciales de la Universidad de Toronto (UTIAS)",
    "name_en": "University of Toronto Institute for Aerospace Studies (UTIAS)",
    "type": "university",
    "name_file": None,
    "description": "El principal centro espacial de Canadá, crucial en el desarrollo de robótica espacial (Canadarm) y microsatélites.",
    "description_en": "Canada's premier space center, crucial in the development of space robotics (Canadarm) and microsatellites.",
    "link": "https://www.utias.utoronto.ca/",
    "show": True
  },
  {
    "slug": "tokyo-aeronautics",
    "name": "Universidad de Tokio - Aeronáutica y Astronáutica",
    "name_en": "University of Tokyo - Department of Aeronautics and Astronautics",
    "type": "university",
    "name_file": None,
    "description": "Centro neurálgico de la investigación espacial asiática, colaborando íntimamente con JAXA en misiones interplanetarias.",
    "description_en": "Hub of Asian space research, collaborating intimately with JAXA on interplanetary missions.",
    "link": "https://www.aero.t.u-tokyo.ac.jp/",
    "show": True
  },
  {
    "slug": "beihang-university",
    "name": "Universidad de Beihang (BUAA)",
    "name_en": "Beihang University (BUAA) - Aeronautic Science and Engineering",
    "type": "university",
    "name_file": None,
    "description": "La principal y más importante universidad aeroespacial de China, pilar fundamental del ambicioso programa espacial del país.",
    "description_en": "China's first and foremost aerospace university, a foundational pillar of the country's ambitious space program.",
    "link": "http://english.buaa.edu.cn/",
    "show": True
  },
  {
    "slug": "tsinghua-aerospace",
    "name": "Universidad de Tsinghua - Escuela de Ingeniería Aeroespacial",
    "name_en": "Tsinghua University - School of Aerospace Engineering",
    "type": "university",
    "name_file": None,
    "description": "Conocida como el 'MIT de China', desarrolla tecnología crítica para vuelos espaciales tripulados e ingeniería astronáutica de élite.",
    "description_en": "Known as the 'MIT of China', it develops critical technology for human spaceflight and elite astronautic engineering.",
    "link": "https://www.hy.tsinghua.edu.cn/",
    "show": True
  },
  {
    "slug": "sydney-aerospace",
    "name": "Universidad de Sídney - Ingeniería Aeroespacial",
    "name_en": "University of Sydney - Aerospace Engineering",
    "type": "university",
    "name_file": None,
    "description": "Líder de la investigación espacial en Oceanía, centrada en vuelos hipersónicos, robótica de exploración y sistemas de vehículos espaciales.",
    "description_en": "Leader in space research in Oceania, focused on hypersonic flight, exploration robotics, and space vehicle systems.",
    "link": "https://www.sydney.edu.au/engineering/study/aerospace-engineering.html",
    "show": True
  },
  {
    "slug": "kth-aerospace",
    "name": "Real Instituto de Tecnología (KTH) - Ingeniería Aeroespacial",
    "name_en": "KTH Royal Institute of Technology - Aerospace Engineering",
    "type": "university",
    "name_file": None,
    "description": "Referente en el norte de Europa, destaca por sus programas de física espacial, tecnología de propulsión y colaboración con la ESA.",
    "description_en": "Benchmark in Northern Europe, known for its space physics programs, propulsion technology, and ESA collaborations.",
    "link": "https://www.kth.se/en/sci/institutioner/farkost/aerospace-engineering-1.1009180",
    "show": True
  }
]

        added_count = 0
        updated_count = 0

        for item in research_data:
            if item["slug"] in existing_slugs:
                # Update existing record
                db.query(models.ResearchDevelopment).filter(models.ResearchDevelopment.slug == item["slug"]).update(item)
                updated_count += 1
            else:
                # Insert new record
                new_item = models.ResearchDevelopment(**item)
                db.add(new_item)
                added_count += 1
        
        db.commit()
        print(f"Success! {added_count} items added, {updated_count} items updated.")
        db.close()
        
    except Exception as e:
        print(f"Error seeding {label} database: {e}")

if __name__ == "__main__":
    # Seed Local DB
    seed_db(LOCAL_URL, "LOCAL")
    
    # Seed Remote DB
    seed_db(REMOTE_URL, "REMOTE")
