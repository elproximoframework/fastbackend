import psycopg2
import json

LOCAL_URL = "postgresql://space_user:space_password@localhost:5433/space_db"
REMOTE_URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"

def dump_companies():
    with open(r"d:\YoutubeElProximoFrameworkEnElEspacio\Web\backendfast\scratch\companies_dump.txt", "w", encoding="utf-8") as f:
        for label, url in [("Local", LOCAL_URL), ("Remote", REMOTE_URL)]:
            f.write(f"--- {label} ---\n")
            try:
                conn = psycopg2.connect(url)
                cur = conn.cursor()
                cur.execute("SELECT id, name FROM companies ORDER BY name")
                results = cur.fetchall()
                for row in results:
                    f.write(f"{row[0]}: {row[1]}\n")
                cur.close()
                conn.close()
            except Exception as e:
                f.write(f"Error {label}: {e}\n")

if __name__ == "__main__":
    dump_companies()
