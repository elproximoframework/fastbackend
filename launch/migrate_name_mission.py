"""
migrate_name_mission.py
───────────────────────
1. Añade la columna `name_mission` a la tabla `launches` (si no existe).
2. Rellena `name_mission` separando el `name` por el carácter '|':
   - La parte izquierda queda como `name` (nombre del cohete).
   - La parte derecha se guarda en `name_mission` (nombre de la misión).
   Ejecuta en ambas bases de datos: local y remota.
"""

import psycopg2

LOCAL_DB_URL  = "postgresql://space_user:space_password@localhost:5433/space_db"
REMOTE_DB_URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"


ADD_COLUMN_SQL = """
ALTER TABLE launches
ADD COLUMN IF NOT EXISTS name_mission TEXT;
"""

BACKFILL_SQL = """
UPDATE launches
SET
    name         = TRIM(SPLIT_PART(name, '|', 1)),
    name_mission = CASE
                       WHEN POSITION('|' IN name) > 0
                       THEN TRIM(SPLIT_PART(name, '|', 2))
                       ELSE NULL
                   END
WHERE name LIKE '%|%' OR name_mission IS NULL;
"""

CHECK_SQL = """
SELECT COUNT(*) FROM launches;
"""

SAMPLE_SQL = """
SELECT name, name_mission FROM launches LIMIT 10;
"""


def migrate(db_url: str, label: str) -> None:
    print(f"\n{'='*60}")
    print(f"  Migrating: {label}")
    print(f"{'='*60}")
    try:
        conn = psycopg2.connect(db_url)
        cur  = conn.cursor()

        # 1. Añadir columna
        print(">> Anadiendo columna name_mission (si no existe)...")
        cur.execute(ADD_COLUMN_SQL)
        conn.commit()
        print("   OK Columna asegurada.")

        # 2. Backfill
        print(">> Rellenando name y name_mission a partir del separador '|'...")
        cur.execute(BACKFILL_SQL)
        rows_updated = cur.rowcount
        conn.commit()
        print(f"   OK {rows_updated} filas actualizadas.")

        # 3. Muestra de resultados
        cur.execute(SAMPLE_SQL)
        rows = cur.fetchall()
        print("\nMuestra de datos:")
        print(f"  {'name':<40} | name_mission")
        print(f"  {'-'*40}-+-{'-'*40}")
        for name, mission in rows:
            print(f"  {str(name):<40} | {mission}")

        cur.close()
        conn.close()
        print(f"\nOK {label} migracion completada.")

    except Exception as e:
        print(f"\nERROR en {label}: {e}")


if __name__ == "__main__":
    migrate(LOCAL_DB_URL,  "Local DB  (localhost:5433)")
    migrate(REMOTE_DB_URL, "Remote DB (Railway)")
    print("\n\nMigracion finalizada.")
