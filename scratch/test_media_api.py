import os
import sys
from fastapi.testclient import TestClient

# Add current directory to path so we can import app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app
from app.database import engine, Base
from app import models

client = TestClient(app)

def test_media_api():
    print("--- Testing Media Hub API ---")
    
    # 1. Check if table exists (or create it)
    print("Ensuring tables are created...")
    # Base.metadata.create_all(bind=engine) # Already done in app/main.py import
    
    # 2. Test GET /api/v1/media
    print("Testing GET /api/v1/media...")
    response = client.get("/api/v1/media")
    assert response.status_code == 200
    data = response.json()
    print(f"Response: {data}")
    assert isinstance(data, list)
    assert len(data) == 0
    print("PASS: Empty list returned (as expected)")

    # 3. Test GET /api/v1/media/categories
    print("Testing GET /api/v1/media/categories...")
    response = client.get("/api/v1/media/categories")
    assert response.status_code == 200
    data = response.json()
    print(f"Response: {data}")
    assert isinstance(data, list)
    assert len(data) == 0
    print("PASS: Empty categories list returned")

    # 4. Test GET /api/v1/media/featured
    print("Testing GET /api/v1/media/featured...")
    response = client.get("/api/v1/media/featured")
    assert response.status_code == 200
    data = response.json()
    print(f"Response: {data}")
    assert isinstance(data, list)
    assert len(data) == 0
    print("PASS: Empty featured list returned")

    # 5. Test GET /api/v1/media/non-existent-slug
    print("Testing GET /api/v1/media/non-existent-slug...")
    response = client.get("/api/v1/media/non-existent-slug")
    assert response.status_code == 404
    print("PASS: 404 returned for non-existent source")

    print("\n--- ALL TESTS PASSED ---")

if __name__ == "__main__":
    test_media_api()
