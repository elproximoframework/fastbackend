from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/api/v1/training", tags=["training"])

@router.get("", response_model=List[schemas.TrainingResponse])
def get_training_list(
    request: Request,
    type: Optional[str] = Query(None, description="Filter by type (grade, master, phd, university)"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    query = db.query(models.Training).filter(models.Training.show == True)
    if type:
        query = query.filter(models.Training.type == type)
    
    return query.offset(skip).limit(limit).all()

@router.get("/{slug}", response_model=schemas.TrainingResponse)
def get_training_by_slug(slug: str, db: Session = Depends(get_db)):
    training = db.query(models.Training).filter(
        models.Training.slug == slug,
        models.Training.show == True
    ).first()
    
    if not training:
        # Fallback to ID if numeric
        if slug.isdigit():
            training = db.query(models.Training).filter(
                models.Training.id == int(slug),
                models.Training.show == True
            ).first()
            
    if not training:
        raise HTTPException(status_code=404, detail="Training record not found")
    
    return training
