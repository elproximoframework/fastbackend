from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/api/v1/shop",
    tags=["shop"]
)

@router.get("", response_model=List[schemas.ShopProductResponse])
def get_shop_products(
    request: Request,
    category: Optional[str] = None,
    featured: Optional[bool] = None,
    skip: int = 0,
    limit: int = 1000,
    db: Session = Depends(get_db)
):
    query = db.query(models.ShopProduct).filter(models.ShopProduct.show == True)
    
    if category:
        query = query.filter(models.ShopProduct.category.ilike(f"%{category}%"))
        
    if featured is not None:
        query = query.filter(models.ShopProduct.featured == featured)
        
    products = query.order_by(models.ShopProduct.id.desc()).offset(skip).limit(limit).all()
    return products

@router.get("/{product_id}", response_model=schemas.ShopProductResponse)
def get_shop_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.ShopProduct).filter(models.ShopProduct.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
