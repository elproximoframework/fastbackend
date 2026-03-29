import psycopg2
import os

DATABASE_URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"

def check_schema():
    print(f"Checking schema for table 'news'...")
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'news'")
        columns = [c[0] for c in cur.fetchall()]
        print(f"Columns in 'news' table: {columns}")
        
        for col in ["body", "body_en"]:
            if col in columns:
                print(f"[!] Column '{col}' STILL EXISTS.")
            else:
                print(f"[✓] Column '{col}' is GONE.")
        
        cur.close()
        conn.close()
    except Exception as e:
        print(f"[!] ERROR: {e}")

if __name__ == "__main__":
    check_schema()
