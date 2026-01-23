"""
Schemas de Pydantic para hábitos.
"""
from typing import Optional
from pydantic import BaseModel, Field


class HabitBase(BaseModel):
    """Campos comunes de hábito."""
    name: str = Field(..., min_length=3, max_length=100, description="Nombre del hábito")
    description: Optional[str] = Field(None, max_length=500, description="Descripción detallada del hábito")
    base_xp: int = Field(default=50, ge=0, le=1000, description="XP base que otorga el hábito")
    base_coins: int = Field(default=10, ge=0, le=500, description="Monedas base que otorga el hábito")


class HabitCreate(HabitBase):
    """Schema para crear un hábito."""
    category_id: int = Field(..., description="ID de la categoría")


class HabitUpdate(BaseModel):
    """Schema para actualizar un hábito."""
    name: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    base_xp: Optional[int] = Field(None, ge=0, le=1000)
    base_coins: Optional[int] = Field(None, ge=0, le=500)
    category_id: Optional[int] = None


class HabitResponse(HabitBase):
    """Schema de respuesta para hábito."""
    id: int
    category_id: int
    
    class Config:
        from_attributes = True


class HabitWithCategoryResponse(HabitResponse):
    """Hábito con información de su categoría."""
    category_name: Optional[str] = None
    category_icon: Optional[str] = None