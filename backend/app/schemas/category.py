"""
Schemas de Pydantic para categorías.
"""
from typing import Optional, List
from pydantic import BaseModel, Field


class CategoryBase(BaseModel):
    """Campos comunes de categoría."""
    name: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="Nombre de la categoría"
    )
    description: Optional[str] = Field(
        None,
        max_length=200,
        description="Descripción de la categoría"
    )
    icon: str = Field(
        default="📝",
        max_length=10,
        description="Emoji o icono de la categoría"
    )


class CategoryCreate(CategoryBase):
    """Schema para crear una categoría."""
    pass  # Usa los mismos campos que CategoryBase


class CategoryResponse(CategoryBase):
    """Schema de respuesta para categoría."""
    id: int
    
    class Config:
        from_attributes = True


class CategoryWithHabitsResponse(CategoryResponse):
    """Categoría con lista de sus hábitos."""
    habits: List["HabitResponse"] = []
    
    class Config:
        from_attributes = True


# Importar después para evitar circular import
from app.schemas.habit import HabitResponse
CategoryWithHabitsResponse.model_rebuild()