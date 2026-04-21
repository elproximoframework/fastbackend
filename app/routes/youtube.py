from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/api/v1/youtube",
    tags=["youtube"]
)

@router.get("/", response_model=List[schemas.YouTubeVideoResponse])
def get_youtube_videos(
    request: Request,
    type: Optional[str] = Query(None, description="Filter by video type"),
    own: Optional[bool] = Query(None, description="Filter by own content"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(models.YouTubeVideo).filter(models.YouTubeVideo.show == True)
    
    if type:
        query = query.filter(models.YouTubeVideo.type == type)
    
    if own is not None:
        query = query.filter(models.YouTubeVideo.own == own)
    
    videos = query.order_by(models.YouTubeVideo.date.desc()).offset(skip).limit(limit).all()
    return videos

@router.get("/types", response_model=List[str])
def get_youtube_video_types(db: Session = Depends(get_db)):
    types = db.query(models.YouTubeVideo.type).distinct().all()
    # Flatten the list of tuples
    return [t[0] for t in types if t[0]]
