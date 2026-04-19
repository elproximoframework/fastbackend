import psycopg2

LOCAL_URL = "postgresql://space_user:space_password@localhost:5433/space_db"
REMOTE_URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"

def check_columns(url_str, name):
    print(f"Checking {name}...")
    try:
        conn = psycopg2.connect(url_str)
        cur = conn.cursor()
        cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'companies'")
        columns = [row[0] for row in cur.fetchall()]
        print(f"Columns in {name}: {columns}")
        if 'validated' in columns:
            print(f"'validated' column exists in {name}")
        else:
            print(f"'validated' column DOES NOT exist in {name}")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error checking {name}: {e}")

if __name__ == "__main__":
    check_columns(LOCAL_URL, "LOCAL")
    check_columns(REMOTE_URL, "REMOTE")
