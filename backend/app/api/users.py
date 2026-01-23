"""
Endpoints relacionados con usuarios.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.utils.auth import get_current_user, get_current_user_id
from app.schemas import UserResponse, UserStatsResponse, UserProfileResponse


router = APIRouter(prefix="/api/users", tags=["Usuarios"])


@router.get("/me", response_model=UserProfileResponse) # <--- Añade esto
async def get_my_profile(user: User = Depends(get_current_user)):
    # Ahora puedes devolver el objeto 'user' directamente dos veces
    # FastAPI usará tus schemas para "limpiar" los campos automáticamente
    return {
        "user": user, 
        "stats": user
    }
@router.get("/me/stats", response_model=UserStatsResponse) # <--- Añade esto
async def get_my_stats(user: User = Depends(get_current_user)):
    return user # ¡Así de simple! Pydantic extrae global_xp, coins, etc.

@router.get("/verify")
async def verify_token(user_id: str = Depends(get_current_user_id)):
    """Verifica que el token es válido y devuelve el user_id."""
    return {"valid": True, "clerk_user_id": user_id}