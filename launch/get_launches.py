"""
get_launches.py
───────────────
Script para consultar los próximos lanzamientos espaciales
usando la API pública de The Space Devs (Launch Library 2 v2.3.0).

Este script está organizado dentro de la carpeta 'launch' del backend.
Documentación: https://ll.thespacedevs.com/docs/
"""

import requests
from datetime import datetime

# Versión 2.3.0 (Plural: launches)
API_BASE = "https://ll.thespacedevs.com/2.3.0"

def obtener_lanzamientos(limit: int = 5) -> list[dict]:
    """Obtiene los próximos lanzamientos espaciales con modo detallado."""
    url = f"{API_BASE}/launches/upcoming/"
    # 'mode': 'detailed' nos da acceso a vid_urls, info_urls y más detalles
    params = {"limit": limit, "format": "json", "mode": "detailed"}

    response = requests.get(url, params=params, timeout=15)
    response.raise_for_status()

    data = response.json()
    return data.get("results", [])

def mostrar_lanzamiento(launch: dict) -> None:
    """Imprime la información de un lanzamiento de forma legible usando v2.3.0."""
    nombre = launch.get("name", "Desconocido")
    estado = launch.get("status", {}).get("name", "N/A")
    fecha_str = launch.get("net")  # NET = No Earlier Than
    
    lsp = launch.get("launch_service_provider", {})
    proveedor = lsp.get("name", "N/A")
    
    rocket = launch.get("rocket", {})
    cohete = rocket.get("configuration", {}).get("full_name", "N/A")
    
    pad = launch.get("pad", {})
    ubicacion = pad.get("location", {}).get("name", "N/A")
    cuerpo_celeste = pad.get("location", {}).get("celestial_body", {}).get("name", "Tierra")
    
    mision = launch.get("mission")
    
    # v2.3.0: vid_urls e info_urls (renombrados de vidURLs/infoURLs)
    vid_urls = launch.get("vid_urls", [])
    info_urls = launch.get("info_urls", [])

    # Formatear fecha
    if fecha_str:
        try:
            fecha = datetime.fromisoformat(fecha_str.replace("Z", "+00:00"))
            fecha_fmt = fecha.strftime("%d/%m/%Y %H:%M UTC")
        except ValueError:
            fecha_fmt = fecha_str
    else:
        fecha_fmt = "Por confirmar"

    print(f"🚀 {nombre}")
    print(f"   Estado      : {estado}")
    print(f"   Fecha (NET) : {fecha_fmt}")
    print(f"   Cuerpo      : {cuerpo_celeste}")
    print(f"   Proveedor   : {proveedor}")
    print(f"   Cohete      : {cohete}")
    print(f"   Ubicación   : {ubicacion}")

    if mision:
        desc = mision.get("description", "Sin descripción")
        tipo = mision.get("type", "N/A")
        orbita = mision.get("orbit", {}).get("name", "N/A") if mision.get("orbit") else "N/A"
        print(f"   Misión      : {mision.get('name', 'N/A')}")
        print(f"   Tipo        : {tipo}")
        print(f"   Órbita      : {orbita}")
        print(f"   Descripción : {desc[:120]}{'...' if len(desc) > 120 else ''}")

    if vid_urls:
        print("   Videos      :")
        for v in vid_urls[:2]: # Mostrar máx 2
            print(f"     - {v.get('url')}")
            
    if info_urls:
        print("   Más info    :")
        for i in info_urls[:2]:
            print(f"     - {i.get('url')}")

    print()

def main():
    print("=" * 60)
    print("  PRÓXIMOS LANZAMIENTOS ESPACIALES (API v2.3.0)")
    print("  Fuente: The Space Devs – Launch Library 2")
    print("=" * 60)
    print()

    try:
        lanzamientos = obtener_lanzamientos(limit=5)

        if not lanzamientos:
            print("No se encontraron lanzamientos próximos.")
            return

        print(f"Mostrando {len(lanzamientos)} lanzamientos próximos:\n")

        for i, launch in enumerate(lanzamientos, 1):
            print(f"── Lanzamiento {i} {'─' * 40}")
            mostrar_lanzamiento(launch)

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            print("⚠️  Límite de peticiones alcanzado (429). Espera un momento e inténtalo de nuevo.")
        else:
            print(f"❌ Error HTTP {e.response.status_code}: {e}")
    except requests.exceptions.ConnectionError:
        print("❌ Error de conexión. Verifica tu acceso a internet.")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    main()
