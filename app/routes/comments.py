from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List
from datetime import datetime, timezone

from .. import models, schemas
from ..auth import get_current_user
from ..database import get_db

router = APIRouter(prefix="/api/v1/comments", tags=["Comments"])

@router.get("/{item_type}/{item_id}", response_model=List[schemas.CommentResponse])
def get_comments(item_type: str, item_id: int, db: Session = Depends(get_db)):
    """
    Get all comments for a specific item (news or newsspacex).
    """
    if item_type not in ["news", "newsspacex"]:
        raise HTTPException(status_code=400, detail="Invalid item type")
    
    comments = (
        db.query(models.Comment)
        .options(joinedload(models.Comment.user))
        .filter(models.Comment.item_type == item_type, models.Comment.item_id == item_id)
        .order_by(models.Comment.created_at.asc())
        .all()
    )
    
    # Map to schema manually or use from_attributes if possible
    # We need to construct the 'author' field which is ForumAuthorSchema
    result = []
    for c in comments:
        author = schemas.ForumAuthorSchema(
            id=c.user.id,
            name=c.user.name,
            email=c.user.email,
            avatar_url=c.user.avatar_url,
            role=c.user.role
        )
        result.append(schemas.CommentResponse(
            id=c.id,
            content=c.content,
            item_type=c.item_type,
            item_id=c.item_id,
            user_id=c.user_id,
            author=author,
            created_at=c.created_at,
            updated_at=c.updated_at
        ))
    
    return result

@router.post("", response_model=schemas.CommentResponse, status_code=status.HTTP_201_CREATED)
def create_comment(
    comment: schemas.CommentCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Create a new comment. User must be authenticated.
    """
    if comment.item_type not in ["news", "newsspacex"]:
        raise HTTPException(status_code=400, detail="Invalid item type")
    
    # Verify item exists
    if comment.item_type == "news":
        item = db.query(models.News).filter(models.News.id == comment.item_id).first()
    else:
        item = db.query(models.NewsSpaceX).filter(models.NewsSpaceX.id == comment.item_id).first()
    
    if not item:
        raise HTTPException(status_code=404, detail="News item not found")

    new_comment = models.Comment(
        content=comment.content,
        user_id=current_user.id,
        item_type=comment.item_type,
        item_id=comment.item_id
    )
    
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    
    # Construct response
    author = schemas.ForumAuthorSchema(
        id=current_user.id,
        name=current_user.name,
        email=current_user.email,
        avatar_url=current_user.avatar_url,
        role=current_user.role
    )
    
    return schemas.CommentResponse(
        id=new_comment.id,
        content=new_comment.content,
        item_type=new_comment.item_type,
        item_id=new_comment.item_id,
        user_id=new_comment.user_id,
        author=author,
        created_at=new_comment.created_at,
        updated_at=new_comment.updated_at
    )

@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Delete a comment. User must be the owner or an admin.
    """
    comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    if comment.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to delete this comment")
    
    db.delete(comment)
    db.commit()
    return None
