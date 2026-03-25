"""
sample_launches.py
──────────────────
Script de ejemplo que consulta los próximos lanzamientos espaciales
usando la API pública de The Space Devs (Launch Library 2).

Documentación: https://ll.thespacedevs.com/docs/
"""

import requests
from datetime import datetime


API_BASE = "https://ll.thespacedevs.com/2.2.0"


def obtener_lanzamientos(limit: int = 10) -> list[dict]:
    """Obtiene los próximos lanzamientos espaciales."""
    url = f"{API_BASE}/launch/upcoming/"
    params = {"limit": limit, "format": "json"}

    response = requests.get(url, params=params, timeout=15)
    response.raise_for_status()

    data = response.json()
    return data.get("results", [])


def mostrar_lanzamiento(launch: dict) -> None:
    """Imprime la información de un lanzamiento de forma legible."""
    nombre = launch.get("name", "Desconocido")
    estado = launch.get("status", {}).get("name", "N/A")
    fecha_str = launch.get("net")  # NET = No Earlier Than
    proveedor = launch.get("launch_service_provider", {}).get("name", "N/A")
    cohete = launch.get("rocket", {}).get("configuration", {}).get("full_name", "N/A")
    pad = launch.get("pad", {})
    ubicacion = pad.get("location", {}).get("name", "N/A")
    mision = launch.get("mission")

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
    print(f"   Estado     : {estado}")
    print(f"   Fecha (NET): {fecha_fmt}")
    print(f"   Proveedor  : {proveedor}")
    print(f"   Cohete     : {cohete}")
    print(f"   Ubicación  : {ubicacion}")

    if mision:
        desc = mision.get("description", "Sin descripción")
        tipo = mision.get("type", "N/A")
        orbita = mision.get("orbit", {}).get("name", "N/A") if mision.get("orbit") else "N/A"
        print(f"   Misión     : {mision.get('name', 'N/A')}")
        print(f"   Tipo       : {tipo}")
        print(f"   Órbita     : {orbita}")
        print(f"   Descripción: {desc[:120]}{'...' if len(desc) > 120 else ''}")

    print()


def main():
    print("=" * 60)
    print("  PRÓXIMOS LANZAMIENTOS ESPACIALES")
    print("  Fuente: The Space Devs – Launch Library 2")
    print("=" * 60)
    print()

    try:
        lanzamientos = obtener_lanzamientos(limit=20)

        if not lanzamientos:
            print("No se encontraron lanzamientos próximos.")
            return

        print(f"Mostrando {len(lanzamientos)} lanzamientos:\n")

        for i, launch in enumerate(lanzamientos, 1):
            print(f"── Lanzamiento {i} {'─' * 40}")
            mostrar_lanzamiento(launch)

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            print("⚠️  Límite de peticiones alcanzado (429). Espera un momento e inténtalo de nuevo.")
        else:
            print(f"❌ Error HTTP: {e}")
    except requests.exceptions.ConnectionError:
        print("❌ Error de conexión. Verifica tu acceso a internet.")
    except requests.exceptions.Timeout:
        print("❌ Tiempo de espera agotado.")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")


if __name__ == "__main__":
    main()
