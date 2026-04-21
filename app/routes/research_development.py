from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/api/v1/research-development", tags=["research-development"])

@router.get("", response_model=List[schemas.ResearchDevelopmentResponse])
def get_research_development_list(
    request: Request,
    type: Optional[str] = Query(None, description="Filter by type (researchcenter, researchmagazine, paper, conference, estateoftheart)"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    query = db.query(models.ResearchDevelopment).filter(models.ResearchDevelopment.show == True)
    if type:
        query = query.filter(models.ResearchDevelopment.type == type)
    
    return query.offset(skip).limit(limit).all()

@router.get("/{slug}", response_model=schemas.ResearchDevelopmentResponse)
def get_research_development_by_slug(slug: str, db: Session = Depends(get_db)):
    item = db.query(models.ResearchDevelopment).filter(
        models.ResearchDevelopment.slug == slug,
        models.ResearchDevelopment.show == True
    ).first()
    
    if not item:
        # Fallback to ID if numeric
        if slug.isdigit():
            item = db.query(models.ResearchDevelopment).filter(
                models.ResearchDevelopment.id == int(slug),
                models.ResearchDevelopment.show == True
            ).first()
            
    if not item:
        raise HTTPException(status_code=404, detail="Research & Development record not found")
    
    return item
