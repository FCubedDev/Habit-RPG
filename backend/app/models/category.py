"""
Modelo Category - Categorías de hábitos.

Categoriza los hábitos en grupos como:
- Deporte
- Lectura
- Productividad
- Salud mental
- etc.
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class Category(Base):
    """
    Modelo de Categoría.
    
    Las categorías son predefinidas (las creamos nosotros).
    Cada hábito pertenece a una categoría.
    """
    __tablename__ = "categories"
    
    # ID de la categoría
    id = Column(Integer, primary_key=True, index=True)
    
    # Nombre de la categoría (ej: "Deporte", "Lectura")
    name = Column(String, unique=True, nullable=False)
    
    # Descripción de la categoría
    description = Column(String, nullable=True)
    
    # Icono (emoji o nombre de icono)
    icon = Column(String, nullable=True, default="📝")
    
    # Relación: una categoría tiene muchos hábitos
    habits = relationship("Habit", back_populates="category")
    
    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}')>"