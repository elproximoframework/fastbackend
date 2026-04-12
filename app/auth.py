import uuid
import os
import resend
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from . import models
from .database import get_db

# ---- Config ----
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "CAMBIA_ESTO_EN_PRODUCCION")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
resend.api_key = os.getenv("RESEND_API_KEY", "")

security = HTTPBearer()


# ---- Token generators ----

def create_magic_token() -> str:
    """UUID único como token temporal de magic link."""
    return str(uuid.uuid4())


def create_access_token(user_id: int, email: str, role: str) -> str:
    """JWT de acceso (vida corta: 60 min por defecto)."""
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": str(user_id), "email": email, "role": role, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token() -> str:
    """Token opaco de larga duración para renovar el JWT."""
    return str(uuid.uuid4()) + str(uuid.uuid4())


# ---- Email sender ----

def send_magic_link_email(to_email: str, token: str, name: str = None):
    """Envía el magic link por email usando Resend."""
    magic_url = f"{FRONTEND_URL}/auth/verify?token={token}"
    greeting = f"Hola {name}," if name else "Hola,"

    try:
        resend.Emails.send({
            "from": os.getenv("EMAIL_FROM", "login@elproximoframework.com"),
            "to": [to_email],
            "subject": "🚀 Tu enlace de acceso al Portal Espacial",
            "html": f"""
            <div style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto;
                        background:#0a0a1a;color:#fff;padding:40px;border-radius:12px;">
                <h1 style="color:#60a5fa;text-align:center;margin-bottom:8px;">🚀 Portal Espacial</h1>
                <p style="color:#9ca3af;text-align:center;margin-top:0;">El próximo framework en el espacio</p>
                <hr style="border:1px solid #1f2937;margin:24px 0;">
                <p style="font-size:16px;">{greeting}</p>
                <p style="color:#d1d5db;">Haz clic en el botón para acceder a tu cuenta.
                   Este enlace es válido durante <strong style="color:#fff;">15 minutos</strong>.</p>
                <div style="text-align:center;margin:32px 0;">
                    <a href="{magic_url}"
                       style="background:linear-gradient(135deg,#3b82f6,#8b5cf6);
                              color:white;padding:16px 32px;text-decoration:none;
                              border-radius:8px;font-size:16px;font-weight:bold;
                              display:inline-block;">
                        ✨ Acceder al Portal
                    </a>
                </div>
                <p style="color:#6b7280;font-size:12px;text-align:center;">
                    Si no solicitaste este enlace, puedes ignorar este email.<br>
                    El enlace expirará automáticamente en 15 minutos.
                </p>
            </div>
            """,
        })
    except Exception as e:
        raise Exception(f"Error enviando email: {str(e)}")


# ---- JWT validation dependencies ----

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> models.User:
    """Dependencia FastAPI: extrae y valida el usuario del JWT Bearer token."""
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token expirado o inválido")

    user = db.query(models.User).filter(models.User.id == int(user_id)).first()
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="Usuario no encontrado o inactivo")
    return user


def require_premium(current_user: models.User = Depends(get_current_user)) -> models.User:
    """Dependencia para rutas exclusivas de premium y admin."""
    if current_user.role not in ("premium", "admin"):
        raise HTTPException(
            status_code=403,
            detail="Necesitas una suscripción premium para acceder a esta sección"
        )
    return current_user


def require_admin(current_user: models.User = Depends(get_current_user)) -> models.User:
    """Dependencia para rutas de administración."""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Solo administradores")
    return current_user
