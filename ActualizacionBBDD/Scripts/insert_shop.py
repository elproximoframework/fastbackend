import argparse
import sys
import os

# Add parent directory to path to import app modules
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(parent_dir)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import ShopProduct
from dotenv import load_dotenv

# Asegurar que se carguen las variables de entorno si se ejecuta directamente
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'))

# Configuración de URLs
LOCAL_DB_URL = os.getenv("DATABASE_URL")
REMOTE_DB_URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"

def insert_product(db_url, name, name_en, description, description_en, price, image, url, category, featured):
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    db = Session()
    try:
        # Verificar si ya existe para evitar duplicados en esta base de datos
        existing = db.query(ShopProduct).filter(ShopProduct.affiliateUrl == url).first()
        if existing:
            print(f"[{db_url}] El producto ya existe (ID={existing.id}), saltando inserción.")
            return

        new_product = ShopProduct(
            name=name,
            name_en=name_en,
            description=description,
            description_en=description_en,
            price=price,
            image=image, 
            affiliateUrl=url,
            category=category,
            featured=featured,
            show=True
        )
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        print(f"[{db_url}] Producto guardado exitosamente: ID={new_product.id}, Nombre='{new_product.name}'")
    except Exception as e:
        print(f"[{db_url}] Error insertando producto: {str(e)}")
        db.rollback()
    finally:
        db.close()

def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Insert a new product into the Shop in database.")
    parser.add_argument("--name", required=True, help="Product name")
    parser.add_argument("--name_en", help="Product name (English)")
    parser.add_argument("--description", required=True, help="Product description")
    parser.add_argument("--description_en", help="Product description (English)")
    parser.add_argument("--price", required=True, help="Product price (e.g., '89.99€')")
    parser.add_argument("--image", required=True, help="Product image FILENAME (e.g., 'model.png')")
    parser.add_argument("--url", required=True, help="Affiliate URL")
    parser.add_argument("--category", required=True, help="Product category")
    parser.add_argument("--featured", type=str2bool, default=False, help="Is it featured? (True/False)")

    args = parser.parse_args()

    # Insertar en base local
    if LOCAL_DB_URL:
        insert_product(
            db_url=LOCAL_DB_URL,
            name=args.name,
            name_en=args.name_en,
            description=args.description,
            description_en=args.description_en,
            price=args.price,
            image=args.image,
            url=args.url,
            category=args.category,
            featured=args.featured
        )
    
    # Insertar en base remota
    insert_product(
        db_url=REMOTE_DB_URL,
        name=args.name,
        name_en=args.name_en,
        description=args.description,
        description_en=args.description_en,
        price=args.price,
        image=args.image,
        url=args.url,
        category=args.category,
        featured=args.featured
    )
