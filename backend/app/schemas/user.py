"""
Schemas de Pydantic para usuarios.

Estos schemas definen cómo se reciben y envían datos de usuarios
a través de la API.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr


# ============================================================
# SCHEMAS BASE
# ============================================================

class UserAttributes(BaseModel):
    strength: int = 10
    stamina: int = 10
    intelligence: int = 10
    charisma: int = 10

class UserBase(BaseModel):
    """
    Campos comunes para todos los schemas de usuario.
    
    Esto evita repetir código en los schemas derivados.
    """
    username: str = Field(
        ...,
        min_length=4,
        max_length=15,
        description="Nombre de usuario (4-15 caracteres)"
    )


# ============================================================
# SCHEMAS DE ENTRADA (Request)
# ============================================================

class UserCreate(UserBase):
    """
    Schema para crear un usuario.
    
    En realidad, Clerk crea los usuarios.
    Este schema se usa para crear usuario vía webhook.
    """
    clerk_user_id: str = Field(..., description="ID del usuario en Clerk")
    email: EmailStr = Field(..., description="Email del usuario")

class UserUpdate(BaseModel):
    """
    Schema para actualizar un usuario.
    
    Todos los campos son opcionales porque solo enviamos
    lo que queremos actualizar.
    """
    username: Optional[str] = Field(
        None,
        min_length=4,
        max_length=15,
        description="Nuevo nombre de usuario"
    )


# ============================================================
# SCHEMAS DE SALIDA (Response)
# ============================================================

class UserResponse(UserBase):
    """
    Schema para devolver información de usuario.
    
    No incluye información sensible (como clerk_user_id).
    """
    id: int
    email: str
    created_at: datetime
    
    class Config:
        from_attributes = True  # Permite crear desde SQLAlchemy model


class UserStatsResponse(BaseModel):
    """
    Schema para estadísticas del usuario.
    """
    global_xp: int
    global_level: int
    strength: int
    stamina: int
    intelligence: int
    charisma: int
    coins: int
    active_habits: int = 0
    total_completions: int = 0
    longest_streak: int = 0


    class Config:
        from_attributes = True  # Permite crear desde SQLAlchemy model


class UserProfileResponse(BaseModel):
    """
    Schema completo del perfil (incluye stats y hábitos).
    """
    user: UserResponse
    stats: UserStatsResponse