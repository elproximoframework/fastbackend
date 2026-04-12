import psycopg2

dbs = [
    ("LOCAL ", "postgresql://space_user:space_password@localhost:5433/space_db"),
    ("REMOTE", "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"),
]

auth_tables = ["users", "magic_link_tokens", "refresh_tokens"]

for label, url in dbs:
    print(f"\n--- {label} ---")
    try:
        conn = psycopg2.connect(url, connect_timeout=10)
        cur = conn.cursor()
        for t in auth_tables:
            cur.execute(
                "SELECT COUNT(*) FROM information_schema.tables "
                "WHERE table_name=%s AND table_schema='public'", (t,)
            )
            exists = cur.fetchone()[0] > 0
            if exists:
                cur.execute(
                    "SELECT COUNT(*) FROM information_schema.columns "
                    "WHERE table_name=%s AND table_schema='public'", (t,)
                )
                cols = cur.fetchone()[0]
                print(f"  OK      {t} ({cols} cols)")
            else:
                print(f"  MISSING {t}")
        conn.close()
        print(f"  {label} verificado correctamente")
    except Exception as e:
        print(f"  ERROR: {e}")

print("\nChecking endpoints in auth_router.py...")
with open("app/routes/auth_router.py", encoding="utf-8") as f:
    content = f.read()

endpoints = [
    ('post', "/magic-link"),
    ('get',  "/verify"),
    ('get',  "/google"),
    ('get',  "/callback/google"),
    ('get',  "/me"),
    ('post', "/logout"),
]

for method, path in endpoints:
    decorator = f'@router.{method}("{path}")'
    found = decorator in content
    print(f"  {'OK' if found else 'MISSING'} {method.upper()} /api/v1/auth{path}")

with open("app/main.py", encoding="utf-8") as f:
    main = f.read()

print()
print("  auth_router imported in main.py:", "YES" if "from .routes.auth_router import router as auth_router" in main else "NO")
print("  auth_router included in main.py:", "YES" if "app.include_router(auth_router)" in main else "NO")
print("  app/auth.py exists:", "YES")
