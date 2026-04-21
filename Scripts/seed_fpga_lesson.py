"""
seed_fpga_lesson.py
===================
Inserta la primera lección del curso de FPGA.
"""

import sys
from sqlalchemy import create_engine, text

# ---- Conexiones ----
LOCAL_DB_URL  = "postgresql://space_user:space_password@localhost:5433/space_db"
REMOTE_DB_URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"

LESSONS_DATA = [
    {
        "namecourse": "FPGA",
        "chapter": "1",
        "lesson": "FPGA vs CPU vs GPU vs ASCI",
        "slug": "fpga-vs-cpu-vs-gpu-vs-asci",
        "url_youtube": "https://youtu.be/8x1g7yyVhCM",
        "markdown_file": None,
        "orden_index": 1
    },
    {
        "namecourse": "FPGA",
        "chapter": "1",
        "lesson": "FPGAs Aplicaciones",
        "slug": "fpgas-aplicaciones",
        "url_youtube": "https://youtu.be/4rPr5KDqi4c",
        "markdown_file": None,
        "orden_index": 2
    },
    {
        "namecourse": "FPGA",
        "chapter": "2",
        "lesson": "El lenguaje de Circuitos (HDL)",
        "slug": "el-lenguaje-de-circuitos-hdl",
        "url_youtube": "https://youtu.be/o5LRpIe5yRw",
        "markdown_file": None,
        "orden_index": 3
    }
]

def seed_database(label: str, db_url: str):
    print(f"\n{'='*60}")
    print(f"  SEEDING {label}")
    print(f"{'='*60}")
    
    try:
        engine = create_engine(db_url, connect_args={"connect_timeout": 10})
        
        with engine.connect() as conn:
            print(f"  [OK] Conexion establecida con {label}")
            
            # Insert statement
            query = text("""
                INSERT INTO course (namecourse, chapter, lesson, slug, url_youtube, markdown_file, orden_index)
                VALUES (:namecourse, :chapter, :lesson, :slug, :url_youtube, :markdown_file, :orden_index)
                ON CONFLICT (slug) DO UPDATE SET
                    namecourse = EXCLUDED.namecourse,
                    chapter = EXCLUDED.chapter,
                    lesson = EXCLUDED.lesson,
                    url_youtube = EXCLUDED.url_youtube,
                    markdown_file = EXCLUDED.markdown_file,
                    orden_index = EXCLUDED.orden_index
            """)
            
            for lesson in LESSONS_DATA:
                conn.execute(query, lesson)
                print(f"  [OK] Leccion '{lesson['lesson']}' procesada.")
            
            conn.commit()
            
        engine.dispose()
        print(f"  [OK] {label} -- COMPLETADO\n")
        return True
        
    except Exception as e:
        print(f"  [ERR] ERROR en {label}:")
        print(f"     {str(e)}\n")
        return False

if __name__ == "__main__":
    print("\n[INFO] SEMBRANDO DATOS DEL CURSO FPGA")
    
    results = []
    results.append(("LOCAL", seed_database("LOCAL", LOCAL_DB_URL)))
    results.append(("REMOTE", seed_database("REMOTE", REMOTE_DB_URL)))
    
    print(f"{'='*60}")
    print("  RESUMEN")
    print(f"{'='*60}")
    for label, ok in results:
        print(f"  [{'OK' if ok else 'ERR'}] {label}")
    print()
