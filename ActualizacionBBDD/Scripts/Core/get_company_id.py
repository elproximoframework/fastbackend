import psycopg2
import sys
import argparse

# Database URLs
LOCAL_URL = "postgresql://space_user:space_password@localhost:5433/space_db"
REMOTE_URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"

def get_company_id(name):
    """
    Search for a company's ID by its name in both Local and Remote databases.
    """
    for label, url in [("Local", LOCAL_URL), ("Remote", REMOTE_URL)]:
        print(f"\n--- Checking {label} ---")
        try:
            conn = psycopg2.connect(url)
            cur = conn.cursor()
            # Case-insensitive search
            cur.execute("SELECT id, name FROM companies WHERE name ILIKE %s", (name,))
            results = cur.fetchall()
            
            if results:
                for row in results:
                    print(f"ID: {row[0]} | Name: {row[1]}")
            else:
                print(f"[!] No company found with name matching '{name}'")
                
            cur.close()
            conn.close()
        except Exception as e:
            print(f"[!] Error in {label}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get company ID by name from Local and Remote databases.")
    parser.add_argument("name", help="Name of the company to search for.")
    args = parser.parse_args()
    
    get_company_id(args.name)
