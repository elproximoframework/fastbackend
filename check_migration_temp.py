from sqlalchemy import create_engine, text

local_url = "postgresql://space_user:space_password@localhost:5433/space_db"
remote_url = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"

def check(url, name):
    print(f"Checking {name}...")
    try:
        engine = create_engine(url)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name='companies' AND column_name='otrassede';")).fetchone()
            if result:
                print(f"Column 'otrassede' exists in {name}")
            else:
                print(f"Column 'otrassede' DOES NOT exist in {name}")
    except Exception as e:
        print(f"Error checking {name}: {e}")

if __name__ == "__main__":
    check(local_url, "Local")
    check(remote_url, "Remote")
