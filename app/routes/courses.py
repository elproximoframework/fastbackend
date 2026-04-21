from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/api/v1/courses", tags=["courses"])

@router.get("/list", response_model=List[str])
def get_unique_courses(db: Session = Depends(get_db)):
    """Obtiene la lista de nombres únicos de los cursos disponibles."""
    courses = db.query(models.Course.namecourse).filter(
        models.Course.show == True
    ).distinct().all()
    return [c[0] for c in courses]

@router.get("/items", response_model=List[schemas.CourseResponse])
def get_course_items(
    namecourse: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Obtiene todas las lecciones, opcionalmente filtradas por nombre de curso."""
    query = db.query(models.Course).filter(models.Course.show == True)
    if namecourse:
        query = query.filter(models.Course.namecourse == namecourse)
    
    return query.order_by(models.Course.orden_index.asc()).all()

@router.get("/{slug}", response_model=schemas.CourseResponse)
def get_course_lesson(slug: str, db: Session = Depends(get_db)):
    """Obtiene los detalles de una lección específica por su slug."""
    lesson = db.query(models.Course).filter(
        models.Course.slug == slug,
        models.Course.show == True
    ).first()
    
    if not lesson:
        raise HTTPException(status_code=404, detail="Lección no encontrada")
    
    return lesson

@router.get("/navigation/{slug}")
def get_lesson_navigation(slug: str, db: Session = Depends(get_db)):
    """Obtiene los slugs de la lección anterior y siguiente para facilitar la navegación."""
    current_lesson = db.query(models.Course).filter(models.Course.slug == slug).first()
    if not current_lesson:
        raise HTTPException(status_code=404, detail="Lección no encontrada")
    
    # Obtener todas las lecciones del mismo curso ordenadas
    lessons = db.query(models.Course.slug).filter(
        models.Course.namecourse == current_lesson.namecourse,
        models.Course.show == True
    ).order_by(models.Course.orden_index.asc()).all()
    
    slugs = [l[0] for l in lessons]
    current_idx = slugs.index(slug)
    
    prev_slug = slugs[current_idx - 1] if current_idx > 0 else None
    next_slug = slugs[current_idx + 1] if current_idx < len(slugs) - 1 else None
    
    return {
        "prev": prev_slug,
        "next": next_slug
    }
