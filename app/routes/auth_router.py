# app/routes/auth_router.py
import os
import httpx
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from pydantic import BaseModel, EmailStr
from urllib.parse import urlencode
from .. import models
from ..database import get_db
from ..auth import (
    create_magic_token,
    create_access_token,
    create_refresh_token,
    send_magic_link_email,
    get_current_user,
)

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

# ---- Pydantic Schemas ----

class MagicLinkRequest(BaseModel):
    email: EmailStr

class UserMeResponse(BaseModel):
    id: int
    email: str
    name: str | None
    role: str
    avatar_url: str | None
    is_verified: bool
    subscription_status: str


# ============================================================
# MAGIC LINK
# ============================================================

@router.post("/magic-link")
async def request_magic_link(body: MagicLinkRequest, db: Session = Depends(get_db)):
    """
    Solicitar un magic link de acceso.
    """
    email = body.email.lower().strip()
    print(f"DEBUG: Intento de Magic Link para: {email}") # <--- DEBUG LOG

    # Buscar o crear usuario
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        user = models.User(email=email, auth_provider="magic_link")
        db.add(user)
        db.commit()
        db.refresh(user)

    # Invalidar tokens anteriores de este email
    db.query(models.MagicLinkToken).filter(
        models.MagicLinkToken.email == email,
        models.MagicLinkToken.used == False
    ).update({"used": True})
    db.commit()

    # Crear nuevo token (15 minutos de TTL)
    token = create_magic_token()
    magic_token = models.MagicLinkToken(
        user_id=user.id,
        token=token,
        email=email,
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=15)
    )
    db.add(magic_token)
    db.commit()

    # Enviar email
    send_magic_link_email(email, token, user.name)

    return {"message": "¡Enlace enviado! Revisa tu bandeja de entrada."}


@router.get("/verify")
async def verify_magic_link(token: str, db: Session = Depends(get_db)):
    """
    Verificar el token del magic link.
    Valida que no esté usado ni expirado, emite JWT + refresh token.
    """
    now = datetime.now(timezone.utc)

    magic_token = db.query(models.MagicLinkToken).filter(
        models.MagicLinkToken.token == token,
        models.MagicLinkToken.used == False,
        models.MagicLinkToken.expires_at > now
    ).first()

    if not magic_token:
        raise HTTPException(status_code=400, detail="Enlace inválido o expirado")

    # Marcar token como usado
    magic_token.used = True
    db.commit()

    # Actualizar usuario
    user = magic_token.user
    user.is_verified = True
    user.last_login_at = now
    db.commit()

    # Generar tokens de sesión
    access_token = create_access_token(user.id, user.email, user.role)
    refresh_token_str = create_refresh_token()

    db.add(models.RefreshToken(
        user_id=user.id,
        token=refresh_token_str,
        expires_at=now + timedelta(days=30)
    ))
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token_str,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "role": user.role,
            "avatar_url": user.avatar_url,
            "subscription_status": user.subscription_status,
            "is_verified": user.is_verified,
        }
    }


# ============================================================
# GOOGLE OAUTH
# ============================================================

@router.get("/google")
async def google_login():
    """Genera la URL de autenticación de Google y la devuelve al frontend."""
    params = {
        "client_id": os.getenv("GOOGLE_CLIENT_ID"),
        "redirect_uri": os.getenv("GOOGLE_REDIRECT_URI"),
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "select_account",
    }
    google_auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}"
    return {"url": google_auth_url}


@router.get("/callback/google")
async def google_callback(code: str, db: Session = Depends(get_db)):
    """
    Callback de Google OAuth.
    Intercambia el code por tokens de Google, obtiene el perfil del usuario,
    crea/actualiza el usuario en DB y emite JWT propio.
    """
    async with httpx.AsyncClient() as client:
        # 1. Intercambiar code por access_token de Google
        token_res = await client.post(
            "https://oauth2.googleapis.com/token",
            data={
                "code": code,
                "client_id": os.getenv("GOOGLE_CLIENT_ID"),
                "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
                "redirect_uri": os.getenv("GOOGLE_REDIRECT_URI"),
                "grant_type": "authorization_code",
            }
        )
        if token_res.status_code != 200:
            raise HTTPException(status_code=400, detail="Error al obtener token de Google")
        token_data = token_res.json()

        # 2. Obtener perfil del usuario de Google
        user_res = await client.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {token_data['access_token']}"}
        )
        if user_res.status_code != 200:
            raise HTTPException(status_code=400, detail="Error al obtener perfil de Google")
        google_user = user_res.json()

    # 3. Buscar o crear usuario en DB
    user = db.query(models.User).filter(
        (models.User.google_id == google_user["id"]) |
        (models.User.email == google_user["email"])
    ).first()

    now = datetime.now(timezone.utc)

    if not user:
        user = models.User(
            email=google_user["email"],
            name=google_user.get("name"),
            avatar_url=google_user.get("picture"),
            google_id=google_user["id"],
            auth_provider="google",
            is_verified=True,
            last_login_at=now
        )
        db.add(user)
    else:
        user.google_id = google_user["id"]
        user.avatar_url = google_user.get("picture")
        if not user.name:
            user.name = google_user.get("name")
        user.is_verified = True
        user.last_login_at = now

    db.commit()
    db.refresh(user)

    # 4. Emitir JWT propio + refresh token → redirigir al frontend
    access_token = create_access_token(user.id, user.email, user.role)
    refresh_token_str = create_refresh_token()

    db.add(models.RefreshToken(
        user_id=user.id,
        token=refresh_token_str,
        expires_at=datetime.now(timezone.utc) + timedelta(days=30)
    ))
    db.commit()

    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")
    return RedirectResponse(
        url=f"{frontend_url}/auth/callback/google?token={access_token}&refresh_token={refresh_token_str}"
    )


# ============================================================
# PERFIL Y SESIÓN
# ============================================================

@router.get("/me", response_model=UserMeResponse)
async def get_me(current_user: models.User = Depends(get_current_user)):
    """Obtener datos del usuario autenticado (requiere JWT válido)."""
    return {
        "id": current_user.id,
        "email": current_user.email,
        "name": current_user.name,
        "role": current_user.role,
        "avatar_url": current_user.avatar_url,
        "is_verified": current_user.is_verified,
        "subscription_status": current_user.subscription_status,
    }


@router.post("/logout")
async def logout(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Revocar todos los refresh tokens del usuario."""
    db.query(models.RefreshToken).filter(
        models.RefreshToken.user_id == current_user.id
    ).update({"revoked": True})
    db.commit()
    return {"message": "Sesión cerrada correctamente"}


@router.delete("/me")
async def delete_account(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Eliminar la cuenta del usuario y todos los datos asociados de forma permanente.
    """
    user_id = current_user.id
    user_email = current_user.email

    try:
        # 1. Eliminar tokens de sesión y acceso
        db.query(models.RefreshToken).filter(models.RefreshToken.user_id == user_id).delete()
        db.query(models.MagicLinkToken).filter(models.MagicLinkToken.user_id == user_id).delete()

        # 2. Eliminar actividad en el foro
        # Borramos primero los likes dados por el usuario
        db.query(models.ForumPostLike).filter(models.ForumPostLike.user_id == user_id).delete()
        
        # Al borrar los posts del usuario, se borrarán en cascada sus likes (aunque ya los borramos arriba por seguridad)
        db.query(models.ForumPost).filter(models.ForumPost.author_id == user_id).delete()
        
        # Al borrar los threads del usuario, se borrarán en cascada sus posts y sus likes
        db.query(models.ForumThread).filter(models.ForumThread.author_id == user_id).delete()

        # 3. Eliminar predicciones en desafíos (asociadas por email)
        db.query(models.Prediction).filter(models.Prediction.email == user_email).delete()

        # 4. Eliminar el usuario
        db.delete(current_user)
        
        db.commit()
        return {"message": "Cuenta eliminada correctamente"}
    
    except Exception as e:
        db.rollback()
        print(f"Error al eliminar cuenta: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno al procesar la eliminación de la cuenta")


# ============================================================
# REFRESH TOKEN
# ============================================================

class RefreshRequest(BaseModel):
    refresh_token: str

class RefreshResponse(BaseModel):
    access_token: str
    token_type: str

@router.post("/refresh", response_model=RefreshResponse)
async def refresh_access_token(body: RefreshRequest, db: Session = Depends(get_db)):
    """
    Renova el access_token usando un refresh_token válido.
    No requiere que el access_token anterior sea válido.
    """
    now = datetime.now(timezone.utc)

    stored = db.query(models.RefreshToken).filter(
        models.RefreshToken.token == body.refresh_token,
        models.RefreshToken.revoked == False,
        models.RefreshToken.expires_at > now
    ).first()

    if not stored:
        raise HTTPException(
            status_code=401,
            detail="Refresh token inválido o expirado. Vuelve a iniciar sesión."
        )

    user = stored.user
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="Usuario no encontrado o inactivo.")

    new_access_token = create_access_token(user.id, user.email, user.role)
    return {"access_token": new_access_token, "token_type": "bearer"}
