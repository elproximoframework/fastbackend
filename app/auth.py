import uuid
import os
import requests
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

# Brevo Config
BREVO_API_KEY = os.getenv("BREVO_API_KEY", "")
EMAIL_FROM = os.getenv("EMAIL_FROM", "mision@elproximoframework.com")

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


# ---- Email helper (Brevo API) ----

def _send_email_brevo(to_email: str, subject: str, html_content: str):
    """Función auxiliar para enviar correos vía la API de Brevo."""
    if not BREVO_API_KEY:
        print("❌ Error: BREVO_API_KEY no configurada")
        return

    url = "https://api.brevo.com/v3/smtp/email"
    headers = {
        "accept": "application/json",
        "api-key": BREVO_API_KEY,
        "content-type": "application/json"
    }
    
    payload = {
        "sender": {"email": EMAIL_FROM, "name": "Portal Espacial"},
        "to": [{"email": to_email}],
        "subject": subject,
        "htmlContent": html_content
    }

    try:
        print(f"DEBUG: Enviando email vía Brevo API a {to_email}...")
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        if response.status_code in [201, 202, 200]:
            print(f"✅ Email enviado correctamente a {to_email} (ID: {response.json().get('messageId')})")
        else:
            print(f"❌ Error de Brevo ({response.status_code}): {response.text}")
    except Exception as e:
        print(f"❌ Error crítico contactando con Brevo: {str(e)}")


# ---- Email senders ----

def send_magic_link_email(to_email: str, token: str, name: str = None):
    """Envía el magic link por email usando la API de Brevo."""
    greeting = f"Hola {name}," if name else "Hola,"
    magic_url = f"{FRONTEND_URL}/auth/callback?token={token}"

    html = f"""
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
    """
    
    try:
        _send_email_brevo(to_email, "🚀 Tu enlace de acceso al Portal Espacial", html)
    except Exception as e:
        raise Exception(f"Error enviando magic link: {str(e)}")


def send_prediction_confirmation(to_email: str, nickname: str, challenge_title: str, prediction_date: str, code: str):
    """Envía la confirmación de la predicción con el código de verificación usando la API de Brevo."""
    html = f"""
    <div style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto;
                background:#0a0a1a;color:#fff;padding:40px;border-radius:24px;
                border: 1px solid #1f2937;">
        <div style="text-align:center;margin-bottom:32px;">
            <h1 style="color:#60a5fa;margin-bottom:8px;font-size:28px;">🚀 Desafío Espacial</h1>
            <p style="color:#9ca3af;margin-top:0;">Confirmación de participación</p>
        </div>
        
        <div style="background:#111827;padding:24px;border-radius:16px;margin-bottom:32px;">
            <p style="color:#d1d5db;margin-top:0;">¡Hola <strong style="color:#fff;">{nickname}</strong>!</p>
            <p style="color:#d1d5db;">Hemos registrado correctamente tu predicción para el desafío:</p>
            <p style="background:linear-gradient(90deg,#3b82f6,#8b5cf6);
                      -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                      font-size:20px;font-weight:bold;margin:16px 0;">
                {challenge_title}
            </p>
            <p style="color:#9ca3af;font-size:14px;">Fecha predicha: <strong style="color:#fff;">{prediction_date}</strong></p>
        </div>

        <div style="text-align:center;border:2px dashed #3b82f6;padding:24px;border-radius:16px;">
            <p style="color:#60a5fa;font-size:12px;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;">Tu Código de Validación</p>
            <p style="font-family:monospace;font-size:32px;font-weight:bold;color:#fff;margin:0;letter-spacing:4px;">
                {code}
            </p>
        </div>

        <p style="color:#9ca3af;font-size:14px;margin-top:32px;line-height:1.6;">
            Conserva este código. Si resultas ganador, te lo pediremos para validar tu identidad y entregarte el premio.
        </p>

        <div style="margin-top:40px;padding-top:40px;border-top:1px solid #1f2937;">
            <h2 style="color:#60a5fa;font-size:18px;margin-bottom:16px;text-transform:uppercase;letter-spacing:1px;font-style:italic;">📜 Normas y Privacidad</h2>
            <div style="margin-bottom:24px;">
                <h3 style="color:#fff;font-size:14px;margin-bottom:8px;">🔒 Uso de tus Datos</h3>
                <p style="color:#9ca3af;font-size:13px;line-height:1.5;margin:0;">
                    Tu privacidad es nuestra prioridad absoluta. No hacemos uso de tus datos para fines externos. Tu email solo se utiliza para verificar tu identidad y contactarte si ganas.
                </p>
            </div>
            <div style="background:#0f172a;padding:20px;border-radius:16px;border:1px solid #1e293b;">
                <h3 style="color:#fff;font-size:14px;margin-bottom:12px;border-bottom:1px solid #1e293b;padding-bottom:8px;text-transform:uppercase;font-style:italic;">Reglas Desafío Espacial</h3>
                <ul style="color:#9ca3af;font-size:12px;line-height:1.6;padding-left:0;list-style:none;margin:0;">
                    <li style="margin-bottom:10px;">1. Cierre en la fecha fijada.</li>
                    <li style="margin-bottom:10px;">2. Resolución por exactitud.</li>
                    <li style="margin-bottom:10px;">3. Validación mediante este código.</li>
                </ul>
            </div>
        </div>
        
        <hr style="border:1px solid #1f2937;margin:40px 0;">
        <p style="color:#4b5563;font-size:11px;text-align:center;line-height:1.4;">
            Este es un mensaje automático del Portal Espacial.<br>
            <strong>El Próximo Framework en el Espacio</strong>
        </p>
    </div>
    """

    try:
        _send_email_brevo(to_email, f"✅ Predicción Confirmada: {challenge_title}", html)
    except Exception as e:
        print(f"Error enviando email de confirmación: {str(e)}")
        # No lanzamos excepción aquí para no bloquear el guardado en DB si falla el mail


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
