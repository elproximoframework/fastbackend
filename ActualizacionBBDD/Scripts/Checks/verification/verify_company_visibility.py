import requests
import psycopg2

BASE_URL = "http://localhost:8000/api/v1"
DB_URL = "postgresql://space_user:space_password@localhost:5433/space_db"

def test_visibility():
    print("--- Testing Company Visibility ---")
    
    # 1. Get initial companies
    try:
        response = requests.get(f"{BASE_URL}/companies?limit=10")
        companies = response.json()
        print(f"Initial companies count: {len(companies)}")
        if not companies:
            print("No companies found.")
            return

        target_company = companies[0]
        company_id = target_company['id']
        company_name = target_company['name']
        print(f"Toggling visibility for: {company_name} (ID: {company_id})")

        # 2. Set show=False in database
        conn = psycopg2.connect(DB_URL)
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute("UPDATE companies SET show = FALSE WHERE id = %s", (company_id,))
        print("Set show = FALSE in database.")

        # 3. Check if it's still in the API response
        response = requests.get(f"{BASE_URL}/companies?limit=10")
        companies_after = response.json()
        ids_after = [c['id'] for c in companies_after]
        
        if company_id not in ids_after:
            print(f"[✓] Success: Company {company_name} is no longer in the API response.")
        else:
            print(f"[!] Failure: Company {company_name} is still in the API response.")

        # 4. Revert changes
        cur.execute("UPDATE companies SET show = TRUE WHERE id = %s", (company_id,))
        print("Reverted show = TRUE in database.")
        
        cur.close()
        conn.close()

    except Exception as e:
        print(f"Error during verification: {e}")

if __name__ == "__main__":
    test_visibility()
