import psycopg2
from psycopg2 import sql
from psycopg2.extras import Json

LOCAL_URL = "postgresql://space_user:space_password@localhost:5433/space_db"
REMOTE_URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"

companies = [
  {
    "name": "Aboa Space Research Oy",
    "type": "corporate",
    "country": "fi",
    "countryName": "Finlandia",
    "city": "Turku",
    "coordinates": {"lat": 60.45, "lng": 22.27},
    "employees": 15,
    "website": "https://asro.fi",
    "description": "Aboa Space Research Oy (ASRO) es una empresa finlandesa líder en el desarrollo de instrumentación avanzada para la monitorización de radiación y sensores de partículas, con contribuciones clave en misiones como Artemis I de la NASA.",
    "description_en": "Aboa Space Research Oy (ASRO) is a leading Finnish company specializing in the development of advanced radiation monitoring instrumentation and particle sensors, with key contributions to missions such as NASA's Artemis I.",
    "founded": 1999,
    "ceo": "Jussi Lehti",
    "sector": "research",
    "tags": ["Space Radiation", "Sensors", "Artemis", "Active Dosimeter", "Particle Instrumentation"],
    "socialLinks": {"linkedin": "https://www.linkedin.com/company/aboa-space-research-oy/"},
    "keyPrograms": ["Artemis I (Orion EAD)", "ALTIUS", "LAGRANGE"],
    "fundingStage": "Private",
    "totalFunding": None,
    "stockTicker": None,
    "otrassede": None,
    "logo": "aboa-space-research.png",
    "featured_espacio": False,
    "show": True
  },
  {
    "name": "Admatis LTD",
    "type": "corporate",
    "country": "hu",
    "countryName": "Hungría",
    "city": "Miskolc",
    "coordinates": {"lat": 48.10, "lng": 20.78},
    "employees": 40,
    "website": "https://www.admatis.com",
    "description": "Admatis (Advanced Materials in Space) es una PYME húngara de ingeniería espacial especializada en el diseño y fabricación de hardware estructural y de control térmico para satélites, incluyendo radiadores y aislamiento multicapa (MLI).",
    "description_en": "Admatis (Advanced Materials in Space) is a Hungarian space-engineering SME specializing in the design and manufacture of satellite thermal-control and structural hardware, including radiators and multi-layer insulation (MLI).",
    "founded": 2000,
    "ceo": "Tamás Bárczy",
    "sector": "satellite_components",
    "tags": ["Thermal Control", "MLI", "Radiators", "Structural Hardware", "Satellite Components"],
    "socialLinks": {"linkedin": "https://www.linkedin.com/company/admatis-ltd/"},
    "keyPrograms": ["Satellite Thermal Hardware", "Radiators", "MLI"],
    "fundingStage": "Private",
    "totalFunding": None,
    "stockTicker": None,
    "otrassede": None,
    "logo": "admatis.png",
    "featured_espacio": False,
    "show": True
  }
]

def run_insertion(url, label):
    print(f"Connecting to {label}...")
    try:
        conn = psycopg2.connect(url)
        cur = conn.cursor()
        for company in companies:
            # Check if exists
            cur.execute("SELECT id FROM companies WHERE name = %s", (company['name'],))
            exists = cur.fetchone()
            
            # Prepare data (exclude id and name for column list)
            data = {k: v for k, v in company.items() if k != 'name' and k != 'id'}
            
            # Identify columns and values
            cols = list(data.keys())
            vals = []
            for k in cols:
                v = data[k]
                if k in ['coordinates', 'tags', 'socialLinks', 'keyPrograms']:
                    vals.append(Json(v))
                else:
                    vals.append(v)
            
            if exists:
                # UPDATE
                # Using identifiers ensures "countryName" is quoted correctly
                set_clauses = [sql.SQL("{} = %s").format(sql.Identifier(k)) for k in cols]
                query = sql.SQL("UPDATE companies SET {} WHERE name = %s").format(
                    sql.SQL(', ').join(set_clauses)
                )
                cur.execute(query, vals + [company['name']])
                print(f"Updated: {company['name']}")
            else:
                # INSERT
                query = sql.SQL("INSERT INTO companies ({}, name) VALUES ({}, %s)").format(
                    sql.SQL(', ').join(map(sql.Identifier, cols)),
                    sql.SQL(', ').join([sql.Placeholder()] * len(vals))
                )
                cur.execute(query, vals + [company['name']])
                print(f"Inserted: {company['name']}")
        
        conn.commit()
        cur.close()
        conn.close()
        print(f"Finished {label} safely.")
    except Exception as e:
        print(f"Error in {label}: {e}")

if __name__ == "__main__":
    run_insertion(LOCAL_URL, "Local")
    run_insertion(REMOTE_URL, "Remote")
