import argparse
import sys
import os

# Add parent directory to path to import app modules
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(parent_dir)

from app.database import SessionLocal
from app.models import ShopProduct

def insert_product(name, description, price, image, url, category, featured):
    db = SessionLocal()
    try:
        new_product = ShopProduct(
            name=name,
            description=description,
            price=price,
            image=image, # Solo el nombre por la convención de Cloudinary
            affiliateUrl=url,
            category=category,
            featured=featured,
            show=True
        )
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        print(f"✅ Producto guardado exitosamente: ID={new_product.id}, Nombre='{new_product.name}'")
    except Exception as e:
        print(f"❌ Error insertando producto: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Insert a new product into the Shop in database.")
    parser.add_argument("--name", required=True, help="Product name")
    parser.add_argument("--description", required=True, help="Product description")
    parser.add_argument("--price", required=True, help="Product price (e.g., '89.99€')")
    parser.add_argument("--image", required=True, help="Product image FILENAME (e.g., 'model.png')")
    parser.add_argument("--url", required=True, help="Affiliate URL")
    parser.add_argument("--category", required=True, help="Product category")
    parser.add_argument("--featured", type=bool, default=False, help="Is it featured? (True/False)")

    args = parser.parse_args()

    insert_product(
        name=args.name,
        description=args.description,
        price=args.price,
        image=args.image,
        url=args.url,
        category=args.category,
        featured=args.featured
    )
