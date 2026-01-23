"""
Schemas de Pydantic para hábitos de usuario.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class UserHabitBase(BaseModel):
    """Campos comunes de hábito de usuario."""
    difficulty_level: int = Field(
        default=3,
        ge=1,
        le=5,
        description="Nivel de dificultad (1=Muy Fácil, 5=Muy Difícil)"
    )


class UserHabitCreate(UserHabitBase):
    """
    Schema para activar un hábito.
    
    El usuario elige qué hábito activar y a qué dificultad.
    """
    habit_id: int = Field(..., description="ID del hábito a activar")


class UserHabitUpdate(BaseModel):
    """
    Schema para actualizar un hábito de usuario.
    
    Por ahora solo permite cambiar la dificultad.
    """
    difficulty_level: Optional[int] = Field(
        None,
        ge=1,
        le=5,
        description="Nuevo nivel de dificultad"
    )
    is_active: Optional[bool] = Field(
        None,
        description="Activar/desactivar el hábito"
    )


class UserHabitResponse(UserHabitBase):
    """
    Schema de respuesta para hábito de usuario.
    """
    id: int
    user_id: int
    habit_id: int
    is_active: bool
    current_streak: int
    longest_streak: int
    total_completions: int
    last_completed_at: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserHabitDetailResponse(UserHabitResponse):
    """
    Hábito de usuario con información del hábito base.
    """
    habit_name: str
    habit_description: Optional[str]
    habit_base_xp: int
    habit_base_coins: int
    category_name: str
    category_icon: str
    
    # XP calculado según dificultad
    calculated_xp: int = 0
    calculated_coins: int = 0


class CompleteHabitResponse(BaseModel):
    """
    Respuesta al completar un hábito.
    
    Incluye información sobre las recompensas ganadas.
    """
    success: bool
    message: str
    
    # Recompensas ganadas
    xp_earned: int
    coins_earned: int
    streak_bonus: int
    
    # Estado actual
    new_streak: int
    new_total_completions: int
    
    # Progreso del usuario
    new_global_xp: int
    new_global_level: int
    level_up: bool = False