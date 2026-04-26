"""
seed_forum.py — Inserta las categorías iniciales del foro.
Ejecutar desde: backendfast/
    python -m ActualizacionBBDD.seed_forum
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from app.database import SessionLocal
from app import models

CATEGORIES = [
    {
        "name": "🚀 SpaceX Hub",
        "slug": "spacex-hub",
        "description": "Noticias, análisis y debate sobre SpaceX, Starship y Falcon.",
        "icon": "🚀",
        "color": "#22d3ee",
        "order": 1,
    },
    {
        "name": "🛸 Tecnología Espacial",
        "slug": "tecnologia-espacial",
        "description": "Propulsión, materiales, electrónica y todo lo técnico.",
        "icon": "🛸",
        "color": "#a78bfa",
        "order": 2,
    },
    {
        "name": "🔭 Astronomía y Ciencia",
        "slug": "astronomia-ciencia",
        "description": "Astrofísica, telescopios, planetas y el universo profundo.",
        "icon": "🔭",
        "color": "#f59e0b",
        "order": 3,
    },
    {
        "name": "🛰️ Misiones e Industria",
        "slug": "misiones-industria",
        "description": "NASA, ESA, CNSA y las últimas misiones en marcha.",
        "icon": "🛰️",
        "color": "#34d399",
        "order": 4,
    },
    {
        "name": "💬 General",
        "slug": "general",
        "description": "Charla libre sobre cualquier tema relacionado con el espacio.",
        "icon": "💬",
        "color": "#f87171",
        "order": 5,
    },
]

def main():
    db = SessionLocal()
    try:
        created = 0
        for cat_data in CATEGORIES:
            existing = db.query(models.ForumCategory).filter(
                models.ForumCategory.slug == cat_data["slug"]
            ).first()
            if existing:
                print(f"  ⚠️  Ya existe: {cat_data['slug']}")
                continue
            cat = models.ForumCategory(**cat_data)
            db.add(cat)
            created += 1
            print(f"  ✅ Creada: {cat_data['name']}")
        db.commit()
        print(f"\n🎯 {created} categorías creadas correctamente.")
    finally:
        db.close()

if __name__ == "__main__":
    main()
