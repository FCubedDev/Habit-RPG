"""
Modelo UserHabit - Relación entre usuarios y hábitos.

Esta es la tabla "pivot" o "intermedia" que conecta:
- Un usuario con los hábitos que ha activado
- Almacena el progreso individual (racha, completados, nivel de dificultad)
"""
from datetime import datetime
from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class UserHabit(Base):
    """
    Modelo de Hábito de Usuario.
    
    Representa la relación N:M entre usuarios y hábitos.
    Cada registro es "un usuario tiene activo un hábito específico".
    
    Aquí guardamos el progreso:
    - Nivel de dificultad elegido
    - Racha actual y máxima
    - Total de veces completado
    - Última vez completado
    """
    __tablename__ = "user_habits"
    
    # ID del registro
    id = Column(Integer, primary_key=True, index=True)
    
    # ============================================================
    # CLAVES FORÁNEAS
    # ============================================================
    
    # ID del usuario que tiene este hábito
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # ID del hábito que el usuario activó
    habit_id = Column(Integer, ForeignKey("habits.id"), nullable=False)
    
    # ============================================================
    # CONFIGURACIÓN DEL USUARIO
    # ============================================================
    
    # Nivel de dificultad elegido (1-5)
    # Afecta al multiplicador de XP:
    # 1 = 0.5x, 2 = 0.75x, 3 = 1.0x, 4 = 1.25x, 5 = 1.5x
    difficulty_level = Column(Integer, default=3, nullable=False)
    
    # ¿Está activo? (el usuario puede desactivar sin eliminar)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # ============================================================
    # ESTADÍSTICAS DE PROGRESO
    # ============================================================
    
    # Racha actual (días consecutivos completando)
    current_streak = Column(Integer, default=0, nullable=False)
    
    # Racha más larga alcanzada
    longest_streak = Column(Integer, default=0, nullable=False)
    
    # Total de veces que se ha completado
    total_completions = Column(Integer, default=0, nullable=False)
    
    # ============================================================
    # TIMESTAMPS
    # ============================================================
    
    # Última vez que se completó este hábito
    last_completed_at = Column(DateTime, nullable=True)
    
    # Fecha de activación del hábito
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # ============================================================
    # RELACIONES
    # ============================================================
    
    # Relación con el usuario dueño
    user = relationship("User", back_populates="user_habits")
    
    # Relación con el hábito plantilla
    habit = relationship("Habit", back_populates="user_habits")
    
    def __repr__(self):
        return f"<UserHabit(user_id={self.user_id}, habit_id={self.habit_id}, streak={self.current_streak})>"