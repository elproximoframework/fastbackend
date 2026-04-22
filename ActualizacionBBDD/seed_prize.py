import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))

def seed_prize_data():
    with engine.connect() as conn:
        conn.execute(text("""
            UPDATE challenges 
            SET prize_description = 'Una maqueta a escala 1:150 de la Starship con acabado en acero inoxidable.',
                prize_description_en = 'A 1:150 scale Starship model with stainless steel finish.',
                prize_image_url = 'https://shop.spacex.com/cdn/shop/products/Starship_Model_1_1024x1024.png'
            WHERE id = 1
        """))
        conn.commit()
        print("Prize data seeded for challenge 1")

if __name__ == "__main__":
    seed_prize_data()
