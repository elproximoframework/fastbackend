from app.database import engine
from sqlalchemy import inspect

inspector = inspect(engine)
columns = inspector.get_columns('predictions')
print("Columnas en 'predictions':")
for col in columns:
    print(f"- {col['name']} ({col['type']})")
