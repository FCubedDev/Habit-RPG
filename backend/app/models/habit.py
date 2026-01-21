"""
Modelo Habit - Hábitos disponibles en el sistema.

Son los "hábitos plantilla" que los usuarios pueden activar.
Definidos por los administradores del sistema.
"""
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Habit(Base):
    """
    Modelo de Hábito.
    
    Un hábito es como una "plantilla":
    - Definido por el sistema
    - Los usuarios lo "activan" creando un UserHabit
    - Tiene XP base que se modifica según dificultad
    """
    __tablename__ = "habits"
    
    # ID del hábito
    id = Column(Integer, primary_key=True, index=True)
    
    # Nombre del hábito (ej: "Hacer 30 min de ejercicio")
    name = Column(String, nullable=False)
    
    # Descripción detallada
    description = Column(String, nullable=True)
    
    # Categoría a la que pertenece (FK = Foreign Key)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    
    # XP base que otorga (se modifica según dificultad del usuario)
    base_xp = Column(Integer, default=50, nullable=False)
    
    # Monedas base que otorga
    base_coins = Column(Integer, default=10, nullable=False)
    
    # Relación inversa: a qué categoría pertenece
    category = relationship("Category", back_populates="habits")
    
    # Relación con user_habits (usuarios que tienen este hábito activo)
    user_habits = relationship("UserHabit", back_populates="habit")
    
    def __repr__(self):
        return f"<Habit(id={self.id}, name='{self.name}')>"