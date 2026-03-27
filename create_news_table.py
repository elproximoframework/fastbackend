import psycopg2
import sys

# Connection Strings
LOCAL_URL = "postgresql://space_user:space_password@localhost:5433/space_db"
REMOTE_URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS news (
    id SERIAL PRIMARY KEY,
    title VARCHAR NOT NULL,
    title_en VARCHAR,
    excerpt TEXT,
    excerpt_en TEXT,
    body TEXT,
    body_en TEXT,
    category VARCHAR,
    category_en VARCHAR,
    location VARCHAR,
    location_en VARCHAR,
    covered BOOLEAN DEFAULT FALSE,
    date VARCHAR,
    image VARCHAR,
    slug VARCHAR UNIQUE,
    tags JSONB,
    tags_en JSONB,
    featured BOOLEAN DEFAULT FALSE,
    linkyoutube VARCHAR,
    rutanoticia VARCHAR,
    timestart INTEGER
);

CREATE INDEX IF NOT EXISTS idx_news_title ON news(title);
CREATE INDEX IF NOT EXISTS idx_news_title_en ON news(title_en);
CREATE INDEX IF NOT EXISTS idx_news_slug ON news(slug);
CREATE INDEX IF NOT EXISTS idx_news_category ON news(category);
CREATE INDEX IF NOT EXISTS idx_news_category_en ON news(category_en);
"""

def run_sql(url, db_name):
    print(f"Connecting to {db_name}...")
    try:
        conn = psycopg2.connect(url)
        conn.autocommit = True
        cur = conn.cursor()
        print(f"Creating news table in {db_name}...")
        cur.execute(CREATE_TABLE_SQL)
        print(f"Success in {db_name}!")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error in {db_name}: {e}")

def main():
    run_sql(LOCAL_URL, "Local DB")
    run_sql(REMOTE_URL, "Remote DB (Railway)")

if __name__ == "__main__":
    main()
