from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/api/v1/media", tags=["media"])

@router.get("", response_model=List[schemas.MediaSourceResponse])
def get_media_sources(
    request: Request,
    category: Optional[str] = Query(None, description="Filter by category"),
    language: Optional[str] = Query(None, description="Filter by language"),
    difficulty: Optional[str] = Query(None, description="Filter by difficulty"),
    search: Optional[str] = Query(None, description="Search by name, tagline or description"),
    featured: Optional[bool] = Query(None, description="Filter by featured status"),
    recommended: Optional[bool] = Query(None, description="Filter by recommended status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(models.MediaSource).filter(models.MediaSource.show == True)

    if category:
        query = query.filter(models.MediaSource.category == category)
    if language:
        query = query.filter(models.MediaSource.language == language)
    if difficulty:
        query = query.filter(models.MediaSource.difficulty == difficulty)
    if featured is not None:
        query = query.filter(models.MediaSource.featured == featured)
    if recommended is not None:
        query = query.filter(models.MediaSource.recommended == recommended)
    
    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            (models.MediaSource.name.ilike(search_filter)) |
            (models.MediaSource.tagline.ilike(search_filter)) |
            (models.MediaSource.tagline_en.ilike(search_filter)) |
            (models.MediaSource.description.ilike(search_filter)) |
            (models.MediaSource.description_en.ilike(search_filter))
        )

    # Order by rating descending and then name
    sources = query.order_by(models.MediaSource.rating.desc(), models.MediaSource.name.asc()).offset(skip).limit(limit).all()
    return sources

@router.get("/featured", response_model=List[schemas.MediaSourceResponse])
def get_featured_media(db: Session = Depends(get_db)):
    """Get editorial featured sources"""
    return db.query(models.MediaSource).filter(
        models.MediaSource.featured == True,
        models.MediaSource.show == True
    ).order_by(models.MediaSource.rating.desc()).all()

@router.get("/categories", response_model=List[schemas.CategoryCount])
def get_media_categories_stats(db: Session = Depends(get_db)):
    """Get category counts for the stats bar"""
    stats = db.query(
        models.MediaSource.category,
        func.count(models.MediaSource.id).label("count")
    ).filter(models.MediaSource.show == True).group_by(models.MediaSource.category).all()
    
    return [{"category": s.category, "count": s.count} for s in stats]

@router.get("/{slug}", response_model=schemas.MediaSourceResponse)
def get_media_source_by_slug(slug: str, db: Session = Depends(get_db)):
    """Get detailed information for a specific source"""
    source = db.query(models.MediaSource).filter(
        models.MediaSource.slug == slug,
        models.MediaSource.show == True
    ).first()
    
    if not source:
        # Fallback to ID if numeric
        if slug.isdigit():
            source = db.query(models.MediaSource).filter(
                models.MediaSource.id == int(slug),
                models.MediaSource.show == True
            ).first()
            
    if not source:
        raise HTTPException(status_code=404, detail="Media source not found")
    
    return source
