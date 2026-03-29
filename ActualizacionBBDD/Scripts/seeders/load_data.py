import os
import re
import json
import psycopg2
from psycopg2.extras import Json

try:
    import chompjs
except ImportError:
    print("Error: El paquete 'chompjs' no está instalado.")
    print("Por favor, instala los requerimientos usando: pip install psycopg2-binary chompjs")
    exit(1)

DB_CONFIG = {
    "dbname": "space_db",
    "user": "space_user",
    "password": "space_password",
    "host": "localhost",
    "port": "5433"
}

def clean_date(val):
    if not val or val == '0':
        return None
    return val

def clean_double(val):
    if val is None or val == 'N/A' or val == '':
        return None
    if isinstance(val, (int, float)):
        return float(val)
    if isinstance(val, str):
        match = re.search(r'([-0-9.,]+)', val)
        if match:
            num_str = match.group(1)
            # Handle forms like 1.500.000, 3.7, 1,5, etc
            if num_str.count('.') > 1:
                num_str = num_str.replace('.', '')
            elif ',' in num_str:
                num_str = num_str.replace('.', '').replace(',', '.')
            try:
                return float(num_str)
            except ValueError:
                return None
    return None

def clean_employees(val):
    if not val or val == 'N/A':
        return None
    val = str(val).split(' ')[0] # "40,000+ (Total)" -> "40,000+"
    match = re.search(r'([0-9,]+)', val)
    if match:
        return int(match.group(1).replace(',', ''))
    return None

def extract_array(filepath, regex_pattern):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    match = re.search(regex_pattern, content, re.DOTALL)
    if match:
        try:
            return chompjs.parse_js_object(match.group(1))
        except Exception as e:
            print(f"Error parsing {filepath}: {e}")
    return []

def main():
    print("Conectando a la base de datos...")
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = True
        cursor = conn.cursor()
    except Exception as e:
        print(f"Error conectando a PostgreSQL: {e}")
        return

    # Limpiar tablas previas (opcional, para evitar duplicados en pruebas)
    cursor.execute("TRUNCATE TABLE launches, satellites, rockets, companies RESTART IDENTITY CASCADE;")
    print("Tablas truncadas.")

    # 1. Cargar Empresas
    print("Cargando Empresas...")
    empresas = extract_array('mockEmpresas.ts', r'export\s+const\s+mockEmpresas.*?=\s*(\[.*?\]);')
    empresa_id_map = {} # Map string ID from TS to DB integer ID
    
    for emp in empresas:
        coords = {"lat": emp.get('lat'), "lng": emp.get('lng')}
        cursor.execute("""
            INSERT INTO companies (name, type, country, "countryName", city, coordinates, employees, website, logo, description, founded, ceo, sector, tags, "socialLinks", "keyPrograms", "fundingStage", "totalFunding", "stockTicker")
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id;
        """, (
            emp.get('name'), emp.get('type'), emp.get('country'), emp.get('countryName'),
            emp.get('city'), Json(coords), clean_employees(emp.get('employees')), emp.get('website'),
            emp.get('logo'), emp.get('description'), emp.get('founded'), emp.get('ceo'),
            emp.get('sector'), Json(emp.get('tags', [])), Json(emp.get('socialLinks', {})),
            Json(emp.get('keyPrograms', [])), emp.get('fundingStage'), emp.get('totalFunding'),
            emp.get('stockTicker')
        ))
        new_id = cursor.fetchone()[0]
        empresa_id_map[emp.get('id')] = new_id
        empresa_id_map[emp.get('name')] = new_id # A veces lo referencian por nombre

    # Función auxiliar para buscar el ID de la empresa por nombre (para cohetes y satélites)
    def find_company_id(name):
        if not name: return None
        for k, v in empresa_id_map.items():
            if isinstance(k, str) and k.lower() in name.lower():
                return v
        return None

    # 2. Cargar Cohetes
    print("Cargando Cohetes...")
    # Cohetes es un Record<'es' | 'en', Rocket[]>. Extraemos todo el objeto y cogemos 'es'
    cohetes_obj = extract_array('mockCohetes.ts', r'export\s+const\s+mockCohetes.*?=\s*(\{.*?\});(?:\s*export|\s*$)')
    cohetes = cohetes_obj.get('es', []) if isinstance(cohetes_obj, dict) else []
    
    for coh in cohetes:
        m_id = find_company_id(coh.get('manufacturer'))
        cursor.execute("""
            INSERT INTO rockets (name, manufacturer_id, country, height, diameter, stages, fuel, "leoCapacity", "gtoCapacity", "firstFlight", "totalLaunches", "successRate", status, image, description, "costPerLaunch", reusable)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """, (
            coh.get('name'), m_id, coh.get('country'), clean_double(coh.get('height')),
            clean_double(coh.get('diameter')), coh.get('stages'), coh.get('fuel'),
            clean_double(coh.get('leoCapacity')), clean_double(coh.get('gtoCapacity')),
            clean_date(coh.get('firstFlight')), coh.get('totalLaunches'),
            clean_double(coh.get('successRate')), coh.get('status'), coh.get('image'),
            coh.get('description'), clean_double(coh.get('costPerLaunch')),
            coh.get('reusable')
        ))

    # 3. Cargar Satélites
    print("Cargando Satélites...")
    satelites = extract_array('mockSatelites.ts', r'export\s+const\s+mockSatelites.*?=\s*(\[.*?\]);')
    
    for sat in satelites:
        op_id = find_company_id(sat.get('operator'))
        cursor.execute("""
            INSERT INTO satellites (name, "noradId", operator_id, purpose, "launchDate", "orbitType", altitude, inclination, description, image, "isFeatured", "funFact")
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """, (
            sat.get('name'), sat.get('noradId'), op_id, sat.get('purpose'),
            clean_date(sat.get('launchDate')), sat.get('orbitType'),
            clean_double(sat.get('altitude')), clean_double(sat.get('inclination')),
            sat.get('description'), sat.get('image'), sat.get('isFeatured', False),
            sat.get('funFact')
        ))

    print("Carga de datos completada exitosamente.")
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
