import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

LOCAL_DB_URL = os.getenv("DATABASE_URL")

def update_product_en():
    if not LOCAL_DB_URL:
        print("Error: DATABASE_URL not found")
        return
        
    engine = create_engine(LOCAL_DB_URL)
    with engine.connect() as conn:
        # Update product with ID 3 (Maqueta Starship)
        query = text("""
            UPDATE shop_products 
            SET name_en = 'Starship Super Heavy Model', 
                description_en = '1:100 scale model of the most powerful rocket ever built. Precision details with Super Heavy.'
            WHERE id = 3;
        """)
        conn.execute(query)
        conn.commit()
        print("Product 3 updated with English translations.")

if __name__ == "__main__":
    update_product_en()
