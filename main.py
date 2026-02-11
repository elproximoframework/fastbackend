from fastapi import FastAPI

app = FastAPI(title="Railway Fast API Example")

@app.get("/")
def read_root():
    return {"message": "¡Hola desde FastAPI en Railway!", "status": "running"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
