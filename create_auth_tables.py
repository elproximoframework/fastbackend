"""
create_auth_tables.py
=====================
Crea las tablas de autenticación (users, magic_link_tokens, refresh_tokens)
en LOCAL y REMOTE PostgreSQL.

Uso:
    python create_auth_tables.py          → crea en LOCAL y REMOTE
    python create_auth_tables.py --local  → solo LOCAL
    python create_auth_tables.py --remote → solo REMOTE
"""

import sys
from sqlalchemy import create_engine, text, inspect

# ---- Conexiones ----
LOCAL_DB_URL  = "postgresql://space_user:space_password@localhost:5433/space_db"
REMOTE_DB_URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"

SQL_TABLES = """
-- =====================================================
-- TABLA: users
-- =====================================================
CREATE TABLE IF NOT EXISTS users (
    id                      SERIAL PRIMARY KEY,
    email                   VARCHAR(255) UNIQUE NOT NULL,
    name                    VARCHAR(255),
    avatar_url              VARCHAR(500),

    -- Roles y suscripción
    role                    VARCHAR(50)  NOT NULL DEFAULT 'free',
    subscription_status     VARCHAR(50)  NOT NULL DEFAULT 'inactive',
    subscription_expires_at TIMESTAMP WITH TIME ZONE,
    subscription_plan       VARCHAR(50),

    -- Proveedor auth
    auth_provider           VARCHAR(50)  NOT NULL DEFAULT 'magic_link',
    google_id               VARCHAR(255) UNIQUE,
    hashed_password         VARCHAR(500),

    -- Estado
    is_active               BOOLEAN NOT NULL DEFAULT TRUE,
    is_verified             BOOLEAN NOT NULL DEFAULT FALSE,
    created_at              TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at              TIMESTAMP WITH TIME ZONE,
    last_login_at           TIMESTAMP WITH TIME ZONE
);

CREATE INDEX IF NOT EXISTS idx_users_email    ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_role     ON users(role);
CREATE INDEX IF NOT EXISTS idx_users_google   ON users(google_id);

-- =====================================================
-- TABLA: magic_link_tokens
-- =====================================================
CREATE TABLE IF NOT EXISTS magic_link_tokens (
    id         SERIAL PRIMARY KEY,
    user_id    INTEGER REFERENCES users(id) ON DELETE CASCADE,
    token      VARCHAR(255) UNIQUE NOT NULL,
    email      VARCHAR(255) NOT NULL,
    purpose    VARCHAR(50)  NOT NULL DEFAULT 'login',
    used       BOOLEAN      NOT NULL DEFAULT FALSE,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_magic_token     ON magic_link_tokens(token);
CREATE INDEX IF NOT EXISTS idx_magic_email     ON magic_link_tokens(email);
CREATE INDEX IF NOT EXISTS idx_magic_used      ON magic_link_tokens(used);

-- =====================================================
-- TABLA: refresh_tokens
-- =====================================================
CREATE TABLE IF NOT EXISTS refresh_tokens (
    id         SERIAL PRIMARY KEY,
    user_id    INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token      VARCHAR(500) UNIQUE NOT NULL,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    revoked    BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE INDEX IF NOT EXISTS idx_refresh_token   ON refresh_tokens(token);
CREATE INDEX IF NOT EXISTS idx_refresh_user    ON refresh_tokens(user_id);
CREATE INDEX IF NOT EXISTS idx_refresh_revoked ON refresh_tokens(revoked);
"""

VERIFY_QUERY = """
SELECT table_name, 
       (SELECT COUNT(*) FROM information_schema.columns 
        WHERE table_name = t.table_name AND table_schema = 'public') AS columns
FROM information_schema.tables t
WHERE table_schema = 'public'
  AND table_name IN ('users', 'magic_link_tokens', 'refresh_tokens')
ORDER BY table_name;
"""


def run_migration(label: str, db_url: str):
    print(f"\n{'='*60}")
    print(f"  {label}")
    print(f"{'='*60}")
    
    try:
        engine = create_engine(db_url, connect_args={"connect_timeout": 10})
        
        with engine.connect() as conn:
            print("  ✅ Conexión establecida")
            
            # Ejecutar SQL
            for statement in SQL_TABLES.split(";"):
                stmt = statement.strip()
                if stmt:
                    conn.execute(text(stmt))
            conn.commit()
            print("  ✅ Tablas y índices creados (o ya existían)")
            
            # Verificar
            result = conn.execute(text(VERIFY_QUERY))
            rows = result.fetchall()
            
            print(f"\n  📋 Tablas de autenticación en {label}:")
            print(f"  {'Tabla':<30} {'Columnas':>8}")
            print(f"  {'-'*40}")
            
            found = {row[0]: row[1] for row in rows}
            expected = ["magic_link_tokens", "refresh_tokens", "users"]
            
            for table in expected:
                if table in found:
                    print(f"  ✅ {table:<28} {found[table]:>6} cols")
                else:
                    print(f"  ❌ {table:<28} NO ENCONTRADA")
        
        engine.dispose()
        print(f"\n  ✅ {label} — MIGRACIÓN COMPLETADA\n")
        return True
        
    except Exception as e:
        print(f"\n  ❌ ERROR en {label}:")
        print(f"     {str(e)}\n")
        return False


def check_endpoints():
    """Verifica que el auth_router tiene todos los endpoints necesarios."""
    import os
    router_path = os.path.join(os.path.dirname(__file__), "app", "routes", "auth_router.py")
    
    print(f"\n{'='*60}")
    print("  VERIFICACIÓN DE ENDPOINTS")
    print(f"{'='*60}")
    
    expected_endpoints = [
        ("POST", "/api/v1/auth/magic-link",     "Solicitar magic link"),
        ("GET",  "/api/v1/auth/verify",          "Verificar token magic link"),
        ("GET",  "/api/v1/auth/google",          "Iniciar OAuth Google"),
        ("GET",  "/api/v1/auth/callback/google", "Callback Google OAuth"),
        ("GET",  "/api/v1/auth/me",              "Perfil del usuario"),
        ("POST", "/api/v1/auth/logout",          "Cerrar sesión"),
    ]
    
    try:
        with open(router_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        all_ok = True
        for method, path, desc in expected_endpoints:
            # Busca el decorador @router.METHOD("path") en el fichero
            route_key = path.replace("/api/v1/auth", "")
            decorator = f'@router.{method.lower()}("{route_key}")'
            found = decorator in content
            status = "✅" if found else "❌"
            if not found:
                all_ok = False
            print(f"  {status} {method:<6} {path:<35} — {desc}")
        
        # Verificar main.py incluye el router
        main_path = os.path.join(os.path.dirname(__file__), "app", "main.py")
        with open(main_path, "r", encoding="utf-8") as f:
            main_content = f.read()
        
        print(f"\n  {'='*40}")
        router_included = "auth_router" in main_content and "include_router" in main_content
        print(f"  {'✅' if router_included else '❌'} auth_router registrado en main.py")
        
        auth_imported = "from .routes.auth_router import router as auth_router" in main_content
        print(f"  {'✅' if auth_imported else '❌'} import correcto en main.py")
        
        models_ok = os.path.exists(os.path.join(os.path.dirname(__file__), "app", "auth.py"))
        print(f"  {'✅' if models_ok else '❌'} app/auth.py existe")
        
        if all_ok and router_included and auth_imported and models_ok:
            print(f"\n  ✅ Todo está correctamente enlazado\n")
        else:
            print(f"\n  ⚠️  Hay elementos pendientes de revisar\n")
            
    except FileNotFoundError as e:
        print(f"  ❌ Archivo no encontrado: {e}\n")


if __name__ == "__main__":
    args = sys.argv[1:]
    
    run_local  = "--remote" not in args  # por defecto corre local
    run_remote = "--local"  not in args  # por defecto corre remote
    
    print("\n🚀 SCRIPT DE MIGRACIÓN — TABLAS DE AUTENTICACIÓN")
    print("   Portal Espacial — FastAPI + PostgreSQL\n")

    results = []
    
    if run_local:
        ok = run_migration("LOCAL  (localhost:5433/space_db)", LOCAL_DB_URL)
        results.append(("LOCAL", ok))
    
    if run_remote:
        ok = run_migration("REMOTE (Railway)", REMOTE_DB_URL)
        results.append(("REMOTE", ok))
    
    # Verificar endpoints
    check_endpoints()
    
    # Resumen final
    print(f"{'='*60}")
    print("  RESUMEN FINAL")
    print(f"{'='*60}")
    for label, ok in results:
        print(f"  {'✅' if ok else '❌'} {label}")
    
    if all(ok for _, ok in results):
        print("\n  🎉 Todo listo. Reinicia el backend para activar los cambios.")
    else:
        print("\n  ⚠️  Revisa los errores anteriores.")
    print()
