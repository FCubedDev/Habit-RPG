"""
Endpoints relacionados con usuarios.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.utils.auth import get_current_user, get_current_user_id


router = APIRouter(prefix="/api/users", tags=["Usuarios"])


@router.get("/me")
async def get_my_profile(user: User = Depends(get_current_user)):
    """
    Obtiene el perfil del usuario autenticado.
    
    Requiere un token JWT de Clerk válido en el header Authorization.
    """
    return {
        "id": user.id,
        "clerk_id": user.clerk_user_id,
        "email": user.email,
        "username": user.username,
        "stats": {
            "level": user.global_level,
            "xp": user.global_xp,
            "coins": user.coins,
            "attributes": {
                "strength": user.strength,
                "stamina": user.stamina,
                "intelligence": user.intelligence,
                "charisma": user.charisma
            }
        },
        "created_at": user.created_at.isoformat()
    }

@router.get("/me/stats")
async def get_my_stats(user: User = Depends(get_current_user)):
    """
    Obtiene estadísticas rápidas del usuario.
    """
    return {
        "level": user.global_level,
        "xp": user.global_xp,
        "coins": user.coins
    }

@router.get("/verify")
async def verify_token(user_id: str = Depends(get_current_user_id)):
    """Verifica que el token es válido y devuelve el user_id."""
    return {"valid": True, "clerk_user_id": user_id}