from fastapi.testclient import TestClient
from app.main import app
import traceback

client = TestClient(app)

def test_news():
    print("Testing /api/v1/news...")
    try:
        response = client.get("/api/v1/news?limit=1")
        if response.status_code == 500:
            print("ERROR 500 DETECTED!")
            # We can't easily see the traceback from the TestClient response itself
            # but we can try to look at the response text or headers
            print(f"Response text: {response.text[:500]}")
        else:
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.json()}")
    except Exception as e:
        print("Exception caught:")
        traceback.print_exc()

if __name__ == "__main__":
    test_news()
