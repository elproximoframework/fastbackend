from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import engine, SessionLocal
import uvicorn
from typing import List

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/test", response_model=List[schemas.NewsSpaceXResponse])
def test_endpoint(db: Session = Depends(get_db)):
    try:
        items = db.query(models.NewsSpaceX).all()
        return items
    except Exception as e:
        print(f"DEBUG ERROR: {e}")
        raise

if __name__ == "__main__":
    import requests
    import threading
    import time

    def run_server():
        uvicorn.run(app, host="127.0.0.1", port=8001)

    thread = threading.Thread(target=run_server, daemon=True)
    thread.start()
    time.sleep(2)
    
    try:
        r = requests.get("http://127.0.0.1:8001/test")
        print(f"Status: {r.status_code}")
        print(f"Response: {r.text}")
    except Exception as e:
        print(f"Request Error: {e}")
