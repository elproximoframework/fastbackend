import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000/api/v1/launches"

def test_filter(start_date, end_date):
    params = {
        "start_date": start_date,
        "end_date": end_date,
        "limit": 10
    }
    print(f"Testing range: {start_date} to {end_date}")
    try:
        response = requests.get(BASE_URL, params=params)
        if response.status_code == 200:
            launches = response.json()
            print(f"Found {len(launches)} launches.")
            for i, l in enumerate(launches):
                print(f"  {i+1}. {l['name']} - NET: {l['net']}")
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    # Test April 2026
    test_filter("2026-04-01T00:00:00Z", "2026-04-30T23:59:59Z")
