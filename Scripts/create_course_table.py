"""
create_course_table.py
======================
Crea la tabla 'course' en LOCAL y REMOTE PostgreSQL.

Campos: id, namecourse, chapter, lesson, slug, url_youtube, markdown_file, orden_index.
"""

import sys
from sqlalchemy import create_engine, text

# ---- Conexiones ----
LOCAL_DB_URL  = "postgresql://space_user:space_password@localhost:5433/space_db"
REMOTE_DB_URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"

SQL_TABLES = """
-- =====================================================
-- TABLA: course
-- =====================================================
CREATE TABLE IF NOT EXISTS course (
    id              SERIAL PRIMARY KEY,
    namecourse      VARCHAR(255) NOT NULL,
    chapter         VARCHAR(255),
    lesson          VARCHAR(255),
    slug            VARCHAR(255) UNIQUE NOT NULL,
    url_youtube     VARCHAR(512),
    markdown_file   TEXT,
    orden_index     INTEGER DEFAULT 0,
    show            BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_course_name    ON course(namecourse);
CREATE INDEX IF NOT EXISTS idx_course_slug    ON course(slug);
CREATE INDEX IF NOT EXISTS idx_course_order   ON course(orden_index);
"""

def run_migration(label: str, db_url: str):
    print(f"\n{'='*60}")
    print(f"  {label}")
    print(f"{'='*60}")
    
    try:
        engine = create_engine(db_url, connect_args={"connect_timeout": 10})
        
        with engine.connect() as conn:
            print("  [OK] Conexion establecida con " + label)
            
            # Ejecutar SQL
            # Nota: Dividimos por ';' para ejecutar sentencias individuales
            for statement in SQL_TABLES.split(";"):
                stmt = statement.strip()
                if stmt:
                    conn.execute(text(stmt))
            conn.commit()
            print("  [OK] Tabla 'course' e indices procesados correctamente.")
            
        engine.dispose()
        print(f"\n  [OK] {label} -- PROCESO COMPLETADO\n")
        return True
        
    except Exception as e:
        print(f"\n  [ERR] ERROR en {label}:")
        print(f"     {str(e)}\n")
        return False


if __name__ == "__main__":
    args = sys.argv[1:]
    
    run_local  = "--remote" not in args
    run_remote = "--local"  not in args
    
    print("\n[INFO] INICIANDO CREACION DE TABLA 'COURSE'")
    
    results = []
    
    if run_local:
        ok = run_migration("LOCAL", LOCAL_DB_URL)
        results.append(("LOCAL", ok))
    
    if run_remote:
        ok = run_migration("REMOTE", REMOTE_DB_URL)
        results.append(("REMOTE", ok))
    
    # Resumen final
    print(f"{'='*60}")
    print("  RESUMEN FINAL")
    print(f"{'='*60}")
    for label, ok in results:
        print(f"  [{'OK' if ok else 'ERR'}] {label}")
    print()
