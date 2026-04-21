import psycopg2
from psycopg2 import sql

LOCAL_URL = "postgresql://space_user:space_password@localhost:5433/space_db"
REMOTE_URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS youtube (
    id SERIAL PRIMARY KEY,
    video_name VARCHAR(255) NOT NULL,
    url VARCHAR(500) NOT NULL,
    type VARCHAR(100),
    description TEXT,
    description_en TEXT,
    date VARCHAR(50),
    show BOOLEAN DEFAULT TRUE
);
"""

def create_table(db_url, name):
    print(f"Connecting to {name} database...")
    try:
        conn = psycopg2.connect(db_url)
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(CREATE_TABLE_SQL)
        print(f"Table 'youtube' created or already exists in {name}.")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error creating table in {name}: {e}")

if __name__ == "__main__":
    # Local
    create_table(LOCAL_URL, "LOCAL")
    # Remote
    create_table(REMOTE_URL, "REMOTE")
