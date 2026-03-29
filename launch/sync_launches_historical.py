"""
sync_launches_historical.py
──────────────────────────
Sincroniza los lanzamientos de la API de The Space Devs (v2.3.0)
desde enero de 2026 hasta la fecha actual.
"""

import requests
import psycopg2
import json
import time
from datetime import datetime

# Configuración
API_BASE = "https://ll.thespacedevs.com/2.3.0"
LOCAL_DB_URL = "postgresql://space_user:space_password@localhost:5433/space_db"
REMOTE_DB_URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"

# Rango de fechas: Desde 1 de Enero de 2026 hasta ahora
START_DATE = "2026-01-01T00:00:00Z"
END_DATE = datetime.utcnow().strftime("%Y-%m-%dT23:59:59Z")

def fetch_historical_launches(start_date, end_date):
    """Obtiene todos los lanzamientos en un rango de fechas usando paginación."""
    all_results = []
    url = f"{API_BASE}/launches"
    params = {
        "net__gte": start_date,
        "net__lte": end_date,
        "limit": 50,
        "offset": 0,
        "format": "json",
        "mode": "detailed"
    }
    
    while True:
        print(f"Fetching offset {params['offset']}...")
        r = requests.get(url, params=params, timeout=30)
        
        if r.status_code == 429:
            print("Rate limit reached. Waiting 30 seconds...")
            time.sleep(30)
            continue
            
        r.raise_for_status()
        data = r.json()
        results = data.get("results", [])
        all_results.extend(results)
        
        if not data.get("next"):
            break
            
        params["offset"] += params["limit"]
        time.sleep(1) # Pequeña espera para no saturar la API
        
    return all_results

def get_mappings(cur):
    cur.execute("SELECT id, name FROM companies")
    companies = {row[1].lower(): row[0] for row in cur.fetchall()}
    cur.execute("SELECT id, name FROM rockets")
    rockets = {row[1].lower(): row[0] for row in cur.fetchall()}
    return companies, rockets

def find_id(name, mapping):
    if not name or not isinstance(name, str): return None
    name_lower = name.lower()
    for key, val in mapping.items():
        if key in name_lower or name_lower in key:
            return val
    return None

def sync_to_db(db_url, data, label="DB"):
    try:
        print(f"Syncing {len(data)} launches to {label}...")
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()
        
        comp_map, rock_map = get_mappings(cur)
        
        for l in data:
            api_id = str(l.get("id"))
            name = str(l.get("name"))
            
            # LSP / Provider
            lsp = l.get("launch_service_provider") or {}
            lsp_name = lsp.get("name")
            provider_id = find_id(lsp_name, comp_map)
            
            # Rocket
            rocket = l.get("rocket") or {}
            config = rocket.get("configuration") or {}
            rocket_name = config.get("full_name")
            rocket_id = find_id(rocket_name, rock_map)
            
            # Times
            net_str = l.get("net")
            net_dt = datetime.fromisoformat(net_str.replace("Z", "+00:00")) if net_str else None
            
            # Status
            status_obj = l.get("status") or {}
            status_name = status_obj.get("name")
            
            # Mission
            mission = l.get("mission") or {}
            m_desc = mission.get("description")
            m_type = mission.get("type")
            orbit_obj = mission.get("orbit") or {}
            orbit_name = orbit_obj.get("name")
            
            # Pads & Location
            pad = l.get("pad") or {}
            pad_name = pad.get("name")
            location = pad.get("location") or {}
            loc_name = location.get("name")
            celestial_obj = location.get("celestial_body") or {}
            celestial = celestial_obj.get("name", "Earth")
            
            # Media
            image_obj = l.get("image")
            image_url = None
            if isinstance(image_obj, dict):
                image_url = image_obj.get("image_url")
            elif isinstance(image_obj, str):
                image_url = image_obj
                
            vid_urls = l.get("vid_urls", [])
            info_urls = l.get("info_urls", [])
            webcast_live = l.get("webcast_live", False)
            
            params = (
                api_id, name, rocket_id, provider_id, net_dt, status_name,
                m_desc, m_type, orbit_name, pad_name, loc_name, celestial,
                image_url, json.dumps(vid_urls), json.dumps(info_urls), webcast_live
            )
            
            query = """
                INSERT INTO launches (
                    api_id, name, rocket_id, provider_id, net, status, 
                    mission_description, mission_type, orbit_name, 
                    pad_name, pad_location, celestial_body, 
                    image, vid_urls, info_urls, webcast_live
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
                ON CONFLICT (api_id) DO UPDATE SET
                    status = EXCLUDED.status,
                    net = EXCLUDED.net,
                    image = EXCLUDED.image,
                    vid_urls = EXCLUDED.vid_urls,
                    info_urls = EXCLUDED.info_urls,
                    webcast_live = EXCLUDED.webcast_live,
                    mission_description = EXCLUDED.mission_description,
                    mission_type = EXCLUDED.mission_type,
                    orbit_name = EXCLUDED.orbit_name,
                    pad_name = EXCLUDED.pad_name,
                    pad_location = EXCLUDED.pad_location,
                    celestial_body = EXCLUDED.celestial_body,
                    show = TRUE;
            """
            
            cur.execute(query, params)
            
        conn.commit()
        print(f"Success {label}!")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Failed {label}: {e}")

def main():
    try:
        print(f"Fetching data from {START_DATE} to {END_DATE}...")
        data = fetch_historical_launches(START_DATE, END_DATE)
        print(f"Retrieved {len(data)} total launches.")
        
        # Sincronizar local
        sync_to_db(LOCAL_DB_URL, data, "Local DB")
        
        # Sincronizar remoto
        sync_to_db(REMOTE_DB_URL, data, "Remote DB (Railway)")
        
    except Exception as e:
        print(f"Main execution failed: {e}")

if __name__ == "__main__":
    main()
