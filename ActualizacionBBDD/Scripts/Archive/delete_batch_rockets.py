import psycopg2
import sys

db_urls = [
    "postgresql://space_user:space_password@localhost:5433/space_db",
    "postgresql://postgres:ZbeRovpXmHByhRHeLscRjNlyxZitKIDL@junction.proxy.rlwy.net:16912/railway"
]

rocket_names = (
    "Hyperbola-1",
    "Hyperbola-2",
    "Jielong-3",
    "Kaituozhe-1",
    "Kaituozhe-2"
)

def delete_rockets():
    for url in db_urls:
        env = "Local" if "localhost" in url else "Remote"
        try:
            conn = psycopg2.connect(url)
            cur = conn.cursor()
            cur.execute("DELETE FROM rockets WHERE name IN %s", (rocket_names,))
            count = cur.rowcount
            conn.commit()
            cur.close()
            conn.close()
            print(f"[OK] {env}: Deleted {count} rockets.")
        except Exception as e:
            print(f"[ERROR] {env}: {str(e)}")

if __name__ == "__main__":
    delete_rockets()
