from sqlalchemy import text
from app.database import engine

with engine.connect() as conn:
    print("Añadiendo columna 'verification_code' a 'predictions'...")
    try:
        conn.execute(text("ALTER TABLE predictions ADD COLUMN verification_code VARCHAR"))
        conn.commit()
        print("Columna añadida con éxito.")
    except Exception as e:
        print(f"Error o la columna ya existe: {e}")
