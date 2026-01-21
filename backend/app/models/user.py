"""
Modelo User - Representa a los usuarios de la aplicación.

Cada usuario tiene:
- Identificación de Clerk (para autenticación)
- Estadísticas globales (XP, nivel, monedas)
- Relación con sus hábitos activos
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    """
    Modelo de Usuario.
    
    El usuario se sincroniza con Clerk a través del clerk_user_id.
    Guardamos aquí las estadísticas de juego (XP, nivel, monedas).
    """
    __tablename__ = "users"
    
    # ============================================================
    # COLUMNAS PRINCIPALES
    # ============================================================
    
    # ID interno de nuestra base de datos
    id = Column(Integer, primary_key=True, index=True)
    
    # ID de Clerk - Conecta con el sistema de autenticación
    # Es único porque un usuario de Clerk = un usuario nuestro
    clerk_user_id = Column(String, unique=True, index=True, nullable=False)
    
    # Email del usuario (viene de Clerk)
    email = Column(String, unique=True, index=True, nullable=False)
    
    # Nombre de usuario elegido
    username = Column(String, nullable=True)
    
    # ============================================================
    # ESTADÍSTICAS DE JUEGO
    # ============================================================
    
    # XP global acumulado de todos los hábitos
    global_xp = Column(Integer, default=0, nullable=False)
    
    # Nivel calculado (basado en XP)
    global_level = Column(Integer, default=1, nullable=False)
    
    #attributes
    strength = Column(Integer, default=10, nullable=False)
    stamina = Column(Integer, default=10, nullable=False)
    intelligence = Column(Integer, default=10, nullable=False)
    charisma = Column(Integer, default=10, nullable=False)
    
    # Monedas virtuales ganadas
    coins = Column(Integer, default=0, nullable=False)
    
    # ============================================================
    # TIMESTAMPS
    # ============================================================
    
    # Fecha de creación del usuario
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Fecha de última actualización
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # ============================================================
    # RELACIONES
    # ============================================================
    
    # Un usuario tiene muchos user_habits (hábitos activos)
    # back_populates conecta esta relación con la del otro modelo
    user_habits = relationship("UserHabit", back_populates="user")

    
    def __repr__(self):
        """Representación legible del objeto."""
        return f"<User(id={self.id}, username='{self.username}', level={self.global_level})>"