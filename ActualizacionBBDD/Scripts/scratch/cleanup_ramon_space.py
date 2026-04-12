import psycopg2

def cleanup():
    urls = [
        "postgresql://space_user:space_password@localhost:5433/space_db",
        "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"
    ]
    for url in urls:
        print(f"Checking {url}")
        conn = psycopg2.connect(url)
        cur = conn.cursor()
        
        # Find the placeholder ID 510
        cur.execute("SELECT name FROM companies WHERE id = 510")
        row510 = cur.fetchone()
        name510 = row510[0] if row510 else None
        print(f"ID 510 name: {name510}")

        # Find any other record with name 'Ramon.Space'
        cur.execute("SELECT id, name FROM companies WHERE name = 'Ramon.Space'")
        others = cur.fetchall()
        for oid, oname in others:
            print(f"Found unexpected record: ID {oid}, Name {oname}")
            if oid != 510:
                print(f"Deleting duplicate record ID {oid}")
                cur.execute("DELETE FROM companies WHERE id = %s", (oid,))
        
        conn.commit()
        cur.close()
        conn.close()

if __name__ == "__main__":
    cleanup()
