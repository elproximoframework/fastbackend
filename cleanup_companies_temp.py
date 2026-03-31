from sqlalchemy import create_engine, text

local_url = "postgresql://space_user:space_password@localhost:5433/space_db"
remote_url = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"

def cleanup(url, name):
    print(f"Cleaning up {name} database...")
    try:
        engine = create_engine(url)
        with engine.connect() as conn:
            # We use CASCADE to handle foreign key dependencies (rockets, satellites, launches)
            conn.execute(text("TRUNCATE TABLE companies CASCADE;"))
            # Reset identity sequence if it exists (Serial column)
            try:
                conn.execute(text("ALTER SEQUENCE companies_id_seq RESTART WITH 1;"))
            except Exception as seq_err:
                # If sequence name is different or doesn't exist, ignore
                print(f"Note: Could not reset sequence on {name}: {seq_err}")
            
            conn.commit()
            print(f"Successfully emptied 'companies' table on {name}")
    except Exception as e:
        print(f"Error cleaning up {name}: {e}")

if __name__ == "__main__":
    cleanup(local_url, "Local")
    cleanup(remote_url, "Remote")
