import requests
import psycopg2
import time

API_URL = "http://localhost:8000/api/v1/news"
DB_URL = "postgresql://space_user:space_password@localhost:5433/space_db"

def verify():
    print("--- Verifying News Visibility ---")
    
    # 1. Get initial news count
    response = requests.get(API_URL)
    initial_news = response.json()
    initial_count = len(initial_news)
    print(f"Initial news count: {initial_count}")
    
    if initial_count == 0:
        print("No news found to test.")
        return

    # 2. Pick the first news item and hide it via DB
    test_item = initial_news[0]
    news_id = test_item['id']
    print(f"Hiding news item ID {news_id}: '{test_item['title']}'")
    
    conn = psycopg2.connect(DB_URL)
    conn.autocommit = True
    cur = conn.cursor()
    
    cur.execute('UPDATE news SET "show" = FALSE WHERE id = %s', (news_id,))
    print("News item hidden in DB.")
    
    # Wait a bit for reload if necessary (though it's direct DB update)
    time.sleep(1)
    
    # 3. Check API again
    response = requests.get(API_URL)
    updated_news = response.json()
    updated_count = len(updated_news)
    print(f"Updated news count: {updated_count}")
    
    # Verify the item is gone
    hidden_item_found = any(item['id'] == news_id for item in updated_news)
    
    if not hidden_item_found and updated_count == initial_count - 1:
        print("[✓] SUCCESS: Hidden news item is NOT in the API response.")
    else:
        print("[!] FAILURE: Hidden news item STILL visible or count mismatch.")
        print(f"Hidden item found: {hidden_item_found}")
    
    # 4. Restore the item
    print(f"Restoring news item ID {news_id}...")
    cur.execute('UPDATE news SET "show" = TRUE WHERE id = %s', (news_id,))
    
    cur.close()
    conn.close()
    print("Verification complete.")

if __name__ == "__main__":
    verify()
