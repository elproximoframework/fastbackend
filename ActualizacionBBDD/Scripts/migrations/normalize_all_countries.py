import psycopg2
import os
import sys
from dotenv import load_dotenv

# Mapeo exhaustivo de variaciones a códigos ISO-2 (Mayúsculas)
COUNTRY_MAP = {
    # Norteamérica
    'Estados Unidos': 'US', 'us': 'US', 'USA': 'US', 'EEUU': 'US', 'United States': 'US',
    'Canadá': 'CA', 'ca': 'CA', 'Canada': 'CA', 'Canadá ': 'CA',
    'México': 'MX', 'mx': 'MX', 'Mexico': 'MX',
    
    # Europa
    'España': 'ES', 'es': 'ES', 'Spain': 'ES',
    'Francia': 'FR', 'fr': 'FR', 'France': 'FR',
    'Alemania': 'DE', 'de': 'DE', 'Germany': 'DE',
    'Reino Unido': 'GB', 'UK': 'GB', 'uk': 'GB', 'gb': 'GB', 'Great Britain': 'GB',
    'Italia': 'IT', 'it': 'IT', 'Italy': 'IT',
    'Países Bajos': 'NL', 'nl': 'NL', 'Netherlands': 'NL',
    'Suecia': 'SE', 'se': 'SE', 'Sweden': 'SE',
    'Finlandia': 'FI', 'fi': 'FI', 'Finland': 'FI',
    'Noruega': 'NO', 'no': 'NO', 'Norway': 'NO',
    'Dinamarca': 'DK', 'dk': 'DK', 'Denmark': 'DK',
    'Bélgica': 'BE', 'be': 'BE', 'Belgium': 'BE',
    'Suiza': 'CH', 'ch': 'CH', 'Switzerland': 'CH',
    'Austria': 'AT', 'at': 'AT',
    'República Checa': 'CZ', 'cz': 'CZ', 'Czech Republic': 'CZ',
    'Rumanía': 'RO', 'ro': 'RO', 'Romania': 'RO',
    'Polonia': 'PL', 'pl': 'PL', 'Poland': 'PL',
    'Portugal': 'PT', 'pt': 'PT',
    'Hungría': 'HU', 'hu': 'HU', 'Hungary': 'HU',
    'Bulgaria': 'BG', 'bg': 'BG',
    'Eslovaquia': 'SK', 'sk': 'SK', 'Slovakia': 'SK',
    'Croacia': 'HR', 'hr': 'HR', 'Croatia': 'HR',
    'Luxemburgo': 'LU', 'lu': 'LU', 'Luxembourg': 'LU',
    'Estonia': 'EE', 'ee': 'EE',
    'Letonia': 'LV', 'lv': 'LV',
    'Lituania': 'LT', 'lt': 'LT',
    'Islandia': 'IS', 'is': 'IS', 'Iceland': 'IS',
    'eu': 'EU',
    
    # Asia
    'Japón': 'JP', 'jp': 'JP', 'Japan': 'JP',
    'China': 'CN', 'cn': 'CN',
    'India': 'IN', 'in': 'IN',
    'Corea del Sur': 'KR', 'kr': 'KR', 'South Korea': 'KR',
    'Singapur': 'SG', 'sg': 'SG', 'Singapore': 'SG',
    'Taiwán': 'TW', 'tw': 'TW', 'Taiwan': 'TW',
    'Israel': 'IL', 'il': 'IL',
    'Indonesia': 'ID', 'id': 'ID',
    'Tailandia': 'TH', 'th': 'TH', 'Thailand': 'TH',
    'Malasia': 'MY', 'my': 'MY', 'Malaysia': 'MY',
    'Arabia Saudita': 'SA', 'sa': 'SA', 'Saudi Arabia': 'SA',
    'EAU': 'AE', 'eau': 'AE', 'UAE': 'AE',
    'Turquía': 'TR', 'tr': 'TR', 'Turkey': 'TR',
    
    # Oceanía
    'Australia': 'AU', 'au': 'AU',
    'Nueva Zelanda': 'NZ', 'nz': 'NZ', 'New Zealand': 'NZ',
    
    # Sudamérica
    'Brasil': 'BR', 'br': 'BR', 'Brazil': 'BR',
    'Argentina': 'AR', 'ar': 'AR',
    'Chile': 'CL', 'cl': 'CL',
    'Colombia': 'CO', 'co': 'CO',
    'Perú': 'PE', 'peru': 'PE',
    'Argentina/Uruguay': 'AR', # Simplificación
    
    # África
    'Sudáfrica': 'ZA', 'za': 'ZA', 'South Africa': 'ZA',
    'Nigeria': 'NG', 'ng': 'NG',
    'Egipto': 'EG', 'eg': 'EG', 'Egypt': 'EG',
    'Ruanda': 'RW', 'rw': 'RW',
    'Kenia': 'KE', 'ke': 'KE',
    
    # Otros
    'Rusia': 'RU', 'ru': 'RU', 'Russia': 'RU',
}

# Nombres descriptivos para countryName (opcional pero recomendado para mantener consistencia)
COUNTRY_NAME_MAP = {
    'US': 'Estados Unidos',
    'CA': 'Canadá',
    'MX': 'México',
    'ES': 'España',
    'FR': 'Francia',
    'DE': 'Alemania',
    'GB': 'Reino Unido',
    'IT': 'Italia',
    'JP': 'Japón',
    'CN': 'China',
    'IN': 'India',
    'AU': 'Australia',
    'NZ': 'Nueva Zelanda',
    'BR': 'Brasil',
    'AR': 'Argentina',
    'CL': 'Chile',
    'CO': 'Colombia',
    'PE': 'Perú',
    'IL': 'Israel',
    'KR': 'Corea del Sur',
    'SG': 'Singapur',
    'TW': 'Taiwán',
    'ZA': 'Sudáfrica',
    'AE': 'Emiratos Árabes Unidos',
    'RU': 'Rusia',
}

def normalize_database(db_url, label):
    print(f"\n>>> INICIANDO NORMALIZACIÓN EN: {label}")
    try:
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()
        
        # Obtener valores actuales únicos para reporte
        cur.execute("SELECT DISTINCT country FROM companies")
        current_values = [row[0] for row in cur.fetchall() if row[0]]
        
        updated_count = 0
        
        for val in current_values:
            if val in COUNTRY_MAP:
                new_code = COUNTRY_MAP[val]
                new_name = COUNTRY_NAME_MAP.get(new_code)
                
                print(f"  - Actualizando '{val}' -> '{new_code}'" + (f" (Nombre: {new_name})" if new_name else ""))
                
                if new_name:
                    cur.execute(
                        "UPDATE companies SET country = %s, \"countryName\" = %s WHERE country = %s",
                        (new_code, new_name, val)
                    )
                else:
                    cur.execute(
                        "UPDATE companies SET country = %s WHERE country = %s",
                        (new_code, val)
                    )
                
                updated_count += cur.rowcount
            else:
                if val and val.isupper() and len(val) == 2:
                    # Ya es un código ISO-2 pero tal vez está en minúsculas en el DB?
                    # (Ya manejamos los minúsculas en el map, pero por si acaso)
                    continue
                else:
                    print(f"  [AVISO] No hay mapeo para: '{val}'")

        conn.commit()
        print(f">>> NORMALIZACIÓN COMPLETADA. Filas afectadas: {updated_count}")
        
        cur.close()
        conn.close()
    except Exception as e:
        print(f"ERROR en {label}: {e}")

if __name__ == "__main__":
    # Cargar variables locales - Retroceder 3 niveles desde backendfast/ActualizacionBBDD/Scripts/migrations/
    env_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", ".env")
    load_dotenv(env_path)
    
    LOCAL_URL = os.getenv("DATABASE_URL")
    REMOTE_URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"
    
    if not LOCAL_URL:
        print("ERROR: No se encontró DATABASE_URL en el .env")
        sys.exit(1)
        
    # Ejecutar Local
    normalize_database(LOCAL_URL, "LOCAL")
    
    # Ejecutar Remoto
    normalize_database(REMOTE_URL, "REMOTO (Railway)")
