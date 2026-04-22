import psycopg2
from sqlalchemy import create_engine, text

LOCAL_URL = "postgresql://space_user:space_password@localhost:5433/space_db"
REMOTE_URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"

def check_local():
    print("Checking local database...")
    engine = create_engine(LOCAL_URL)
    with engine.connect() as conn:
        # Check challenges
        res = conn.execute(text("SELECT count(*) FROM challenges"))
        print(f"Challenges count: {res.scalar()}")
        
        # Check predictions
        res = conn.execute(text("SELECT count(*) FROM predictions"))
        print(f"Predictions count: {res.scalar()}")

def check_remote():
    print("\nChecking remote database...")
    try:
        engine = create_engine(REMOTE_URL)
        with engine.connect() as conn:
            # Check if tables exist
            res = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"))
            tables = [r[0] for r in res]
            print(f"Remote tables: {tables}")
    except Exception as e:
        print(f"Error connecting to remote: {e}")

if __name__ == "__main__":
    check_local()
    check_remote()
