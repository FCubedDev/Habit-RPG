"""
Endpoints para recibir webhooks de Clerk.

Los webhooks notifican a nuestro backend cuando ocurren eventos
en Clerk (usuario creado, actualizado, eliminado).
"""
import json
import hmac
import hashlib
from fastapi import APIRouter, Request, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.config import settings


router = APIRouter(prefix="/webhooks", tags=["Webhooks"])


def verify_webhook_signature(payload: bytes, signature: str) -> bool:
    """
    Verifica que el webhook realmente viene de Clerk.
    
    Clerk firma los webhooks con un secret compartido.
    Debemos verificar la firma para asegurarnos de que es legítimo.
    """
    if not settings.clerk_webhook_secret:
        # En desarrollo, podemos saltarnos la verificación
        return True
    
    # Clerk usa HMAC-SHA256 para firmar
    expected = hmac.new(settings.clerk_webhook_secret.encode(),payload,hashlib.sha256).hexdigest()
    
    return hmac.compare_digest(f"sha256={expected}", signature)


@router.post("/clerk")
async def clerk_webhook(request: Request, db: Session = Depends(get_db)):
    """
    Recibe webhooks de Clerk.
    
    Eventos soportados:
    - user.created: Crea usuario en nuestra BD
    - user.updated: Actualiza usuario en nuestra BD
    - user.deleted: Marca usuario como eliminado
    """
    # Obtener el body raw para verificar firma
    payload = await request.body()
    
    # Verificar firma (header: svix-signature)
    signature = request.headers.get("svix-signature", "")
    
    if not verify_webhook_signature(payload, signature):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Firma de webhook inválida"
        )
    
    # Parsear el evento
    try:
        event = json.loads(payload)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payload inválido"
        )
    
    event_type = event.get("type")
    data = event.get("data", {})
    
    # ============================================================
    # MANEJAR EVENTOS
    # ============================================================
    
    if event_type == "user.created":
        return await handle_user_created(data, db)
    
    elif event_type == "user.updated":
        return await handle_user_updated(data, db)
    
    elif event_type == "user.deleted":
        return await handle_user_deleted(data, db)
    
    # Evento no manejado (lo ignoramos)
    return {"status": "ignored", "event": event_type}


async def handle_user_created(data: dict, db: Session):
    """
    Maneja el evento 'user.created'.
    
    Crea un nuevo usuario en nuestra base de datos.
    """
    clerk_user_id = data.get("id")
    email = data.get("email_addresses", [{}])[0].get("email_address")
    username = data.get("username") or data.get("first_name") or "Usuario"
    
    # Verificar que no exista ya
    existing = db.query(User).filter(User.clerk_user_id == clerk_user_id).first()
    if existing:
        return {"status": "already_exists", "user_id": existing.id}
    
    # Crear usuario
    new_user = User(
        clerk_user_id=clerk_user_id,
        email=email,
        username=username,
        global_xp=0,
        global_level=1,
        coins=0
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"status": "created", "user_id": new_user.id}


async def handle_user_updated(data: dict, db: Session):
    """
    Maneja el evento 'user.updated'.
    
    Actualiza los datos del usuario en nuestra BD.
    """
    clerk_user_id = data.get("id")
    email = data.get("email_addresses", [{}])[0].get("email_address")
    username = data.get("username") or data.get("first_name")
    
    user = db.query(User).filter(User.clerk_user_id == clerk_user_id).first()
    
    if not user:
        # Usuario no existe, crearlo
        return await handle_user_created(data, db)
    
    # Actualizar campos
    if email:
        user.email = email
    if username:
        user.username = username
    
    db.commit()
    
    return {"status": "updated", "user_id": user.id}


async def handle_user_deleted(data: dict, db: Session):
    """
    Maneja el evento 'user.deleted'.
    
    En lugar de eliminar, podríamos marcar como inactivo.
    Por ahora, eliminamos el usuario.
    """
    clerk_user_id = data.get("id")
    
    user = db.query(User).filter(User.clerk_user_id == clerk_user_id).first()
    
    if not user:
        return {"status": "not_found"}
    
    db.delete(user)
    db.commit()
    
    return {"status": "deleted", "user_id": user.id}
