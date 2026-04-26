"""
Forum API Router
GET  /api/v1/forum/categories              → lista de categorías (público)
GET  /api/v1/forum/categories/{slug}       → hilos de una categoría (paginado, público)
GET  /api/v1/forum/threads/{slug}          → detalle hilo + posts (paginado, público)
POST /api/v1/forum/threads                 → crear hilo [AUTH]
POST /api/v1/forum/threads/{id}/posts      → responder hilo [AUTH]
POST /api/v1/forum/posts/{id}/like         → toggle like [AUTH]
"""

import re
from datetime import datetime, timezone
from math import ceil
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from .. import models, schemas
from ..auth import get_current_user
from ..database import get_db

router = APIRouter(prefix="/api/v1/forum", tags=["Forum"])


# ── Helpers ───────────────────────────────────────────────────

def _slugify(text: str) -> str:
    """Convierte un título a slug URL-safe."""
    text = text.lower().strip()
    text = re.sub(r"[áàä]", "a", text)
    text = re.sub(r"[éèë]", "e", text)
    text = re.sub(r"[íìï]", "i", text)
    text = re.sub(r"[óòö]", "o", text)
    text = re.sub(r"[úùü]", "u", text)
    text = re.sub(r"[ñ]", "n", text)
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"[\s]+", "-", text)
    return text[:200]


def _unique_slug(base: str, db: Session) -> str:
    """Garantiza que el slug no existe en forum_threads."""
    slug = base
    i = 1
    while db.query(models.ForumThread).filter(models.ForumThread.slug == slug).first():
        slug = f"{base}-{i}"
        i += 1
    return slug


def _build_author(user: models.User) -> schemas.ForumAuthorSchema:
    return schemas.ForumAuthorSchema(
        id=user.id,
        name=user.name,
        email=user.email,
        avatar_url=user.avatar_url,
        role=user.role,
    )


def _build_thread_summary(
    thread: models.ForumThread,
    db: Session
) -> schemas.ForumThreadSummaryResponse:
    post_count = db.query(func.count(models.ForumPost.id)).filter(
        models.ForumPost.thread_id == thread.id
    ).scalar() or 0

    return schemas.ForumThreadSummaryResponse(
        id=thread.id,
        title=thread.title,
        slug=thread.slug,
        author=_build_author(thread.author),
        category_slug=thread.category.slug,
        post_count=post_count,
        views=thread.views,
        is_pinned=thread.is_pinned,
        is_locked=thread.is_locked,
        created_at=thread.created_at,
        updated_at=thread.updated_at,
    )


def _build_post(
    post: models.ForumPost,
    current_user_id: Optional[int],
    db: Session
) -> schemas.ForumPostResponse:
    like_count = db.query(func.count(models.ForumPostLike.id)).filter(
        models.ForumPostLike.post_id == post.id
    ).scalar() or 0

    user_has_liked = False
    if current_user_id:
        user_has_liked = db.query(models.ForumPostLike).filter(
            models.ForumPostLike.post_id == post.id,
            models.ForumPostLike.user_id == current_user_id,
        ).first() is not None

    return schemas.ForumPostResponse(
        id=post.id,
        content=post.content,
        thread_id=post.thread_id,
        author=_build_author(post.author),
        like_count=like_count,
        user_has_liked=user_has_liked,
        created_at=post.created_at,
        updated_at=post.updated_at,
    )


# ── ENDPOINTS ─────────────────────────────────────────────────

@router.get("/categories", response_model=List[schemas.ForumCategoryResponse])
def list_categories(db: Session = Depends(get_db)):
    """Lista todas las categorías activas con contadores."""
    categories = (
        db.query(models.ForumCategory)
        .filter(models.ForumCategory.is_active == True)
        .order_by(models.ForumCategory.order)
        .all()
    )
    result = []
    for cat in categories:
        thread_count = db.query(func.count(models.ForumThread.id)).filter(
            models.ForumThread.category_id == cat.id
        ).scalar() or 0

        post_count = (
            db.query(func.count(models.ForumPost.id))
            .join(models.ForumThread, models.ForumPost.thread_id == models.ForumThread.id)
            .filter(models.ForumThread.category_id == cat.id)
            .scalar() or 0
        )

        result.append(schemas.ForumCategoryResponse(
            id=cat.id,
            name=cat.name,
            slug=cat.slug,
            description=cat.description,
            icon=cat.icon,
            color=cat.color,
            order=cat.order,
            thread_count=thread_count,
            post_count=post_count,
        ))
    return result


@router.get("/categories/{slug}", response_model=schemas.PaginatedThreadsResponse)
def list_threads_by_category(
    slug: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Hilos de una categoría, paginados. Pinneados primero."""
    category = db.query(models.ForumCategory).filter(
        models.ForumCategory.slug == slug,
        models.ForumCategory.is_active == True,
    ).first()
    if not category:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")

    base_q = (
        db.query(models.ForumThread)
        .options(joinedload(models.ForumThread.author), joinedload(models.ForumThread.category))
        .filter(models.ForumThread.category_id == category.id)
    )
    total = base_q.count()
    threads = (
        base_q
        .order_by(models.ForumThread.is_pinned.desc(), models.ForumThread.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    return schemas.PaginatedThreadsResponse(
        items=[_build_thread_summary(t, db) for t in threads],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=ceil(total / page_size) if total else 1,
    )


@router.get("/threads/{slug}", response_model=schemas.ForumThreadDetailResponse)
def get_thread(slug: str, db: Session = Depends(get_db)):
    """Detalle de un hilo. Incrementa el contador de vistas."""
    thread = (
        db.query(models.ForumThread)
        .options(
            joinedload(models.ForumThread.author),
            joinedload(models.ForumThread.category),
        )
        .filter(models.ForumThread.slug == slug)
        .first()
    )
    if not thread:
        raise HTTPException(status_code=404, detail="Hilo no encontrado")

    # Incrementar vistas
    thread.views = (thread.views or 0) + 1
    db.commit()

    cat = thread.category
    post_count = db.query(func.count(models.ForumPost.id)).filter(
        models.ForumPost.thread_id == thread.id
    ).scalar() or 0

    cat_schema = schemas.ForumCategoryResponse(
        id=cat.id, name=cat.name, slug=cat.slug, description=cat.description,
        icon=cat.icon, color=cat.color, order=cat.order,
    )

    return schemas.ForumThreadDetailResponse(
        id=thread.id,
        title=thread.title,
        slug=thread.slug,
        content=thread.content,
        author=_build_author(thread.author),
        category_slug=cat.slug,
        category=cat_schema,
        post_count=post_count,
        views=thread.views,
        is_pinned=thread.is_pinned,
        is_locked=thread.is_locked,
        created_at=thread.created_at,
        updated_at=thread.updated_at,
    )


@router.get("/threads/{slug}/posts", response_model=schemas.PaginatedPostsResponse)
def list_posts(
    slug: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: Optional[models.User] = Depends(lambda: None),
):
    """Posts de un hilo, paginados cronológicamente."""
    thread = db.query(models.ForumThread).filter(models.ForumThread.slug == slug).first()
    if not thread:
        raise HTTPException(status_code=404, detail="Hilo no encontrado")

    base_q = (
        db.query(models.ForumPost)
        .options(joinedload(models.ForumPost.author))
        .filter(models.ForumPost.thread_id == thread.id)
    )
    total = base_q.count()
    posts = base_q.order_by(models.ForumPost.created_at.asc()).offset((page - 1) * page_size).limit(page_size).all()

    uid = current_user.id if current_user else None
    return schemas.PaginatedPostsResponse(
        items=[_build_post(p, uid, db) for p in posts],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=ceil(total / page_size) if total else 1,
    )


@router.post("/threads", response_model=schemas.ForumThreadDetailResponse, status_code=201)
def create_thread(
    body: schemas.CreateThreadRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Crear un nuevo hilo. Requiere autenticación."""
    category = db.query(models.ForumCategory).filter(
        models.ForumCategory.id == body.category_id,
        models.ForumCategory.is_active == True,
    ).first()
    if not category:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")

    if len(body.title.strip()) < 5:
        raise HTTPException(status_code=422, detail="El título debe tener al menos 5 caracteres")
    if len(body.content.strip()) < 20:
        raise HTTPException(status_code=422, detail="El contenido debe tener al menos 20 caracteres")

    base_slug = _slugify(body.title)
    slug = _unique_slug(base_slug, db)

    thread = models.ForumThread(
        title=body.title.strip(),
        slug=slug,
        content=body.content.strip(),
        category_id=body.category_id,
        author_id=current_user.id,
    )
    db.add(thread)
    db.commit()
    db.refresh(thread)

    # Recargar con relaciones
    thread = (
        db.query(models.ForumThread)
        .options(joinedload(models.ForumThread.author), joinedload(models.ForumThread.category))
        .filter(models.ForumThread.id == thread.id)
        .first()
    )

    cat = thread.category
    cat_schema = schemas.ForumCategoryResponse(
        id=cat.id, name=cat.name, slug=cat.slug, description=cat.description,
        icon=cat.icon, color=cat.color, order=cat.order,
    )

    return schemas.ForumThreadDetailResponse(
        id=thread.id, title=thread.title, slug=thread.slug, content=thread.content,
        author=_build_author(thread.author), category_slug=cat.slug, category=cat_schema,
        post_count=0, views=0, is_pinned=False, is_locked=False,
        created_at=thread.created_at, updated_at=None,
    )


@router.post("/threads/{thread_id}/posts", response_model=schemas.ForumPostResponse, status_code=201)
def create_post(
    thread_id: int,
    body: schemas.CreatePostRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Responder a un hilo. Requiere autenticación."""
    thread = db.query(models.ForumThread).filter(models.ForumThread.id == thread_id).first()
    if not thread:
        raise HTTPException(status_code=404, detail="Hilo no encontrado")
    if thread.is_locked:
        raise HTTPException(status_code=403, detail="Este hilo está cerrado y no acepta respuestas")
    if len(body.content.strip()) < 10:
        raise HTTPException(status_code=422, detail="La respuesta debe tener al menos 10 caracteres")

    post = models.ForumPost(
        content=body.content.strip(),
        thread_id=thread_id,
        author_id=current_user.id,
    )
    db.add(post)
    db.commit()
    db.refresh(post)

    post = (
        db.query(models.ForumPost)
        .options(joinedload(models.ForumPost.author))
        .filter(models.ForumPost.id == post.id)
        .first()
    )
    return _build_post(post, current_user.id, db)


@router.post("/posts/{post_id}/like", status_code=200)
def toggle_like(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Toggle like en un post. Devuelve el nuevo estado."""
    post = db.query(models.ForumPost).filter(models.ForumPost.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post no encontrado")

    existing = db.query(models.ForumPostLike).filter(
        models.ForumPostLike.post_id == post_id,
        models.ForumPostLike.user_id == current_user.id,
    ).first()

    if existing:
        db.delete(existing)
        db.commit()
        liked = False
    else:
        db.add(models.ForumPostLike(post_id=post_id, user_id=current_user.id))
        db.commit()
        liked = True

    like_count = db.query(func.count(models.ForumPostLike.id)).filter(
        models.ForumPostLike.post_id == post_id
    ).scalar() or 0

    return {"liked": liked, "like_count": like_count}
