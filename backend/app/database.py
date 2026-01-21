"""
Configuración de la base de datos.

Este archivo maneja la conexión a Supabase y las sesiones de SQLAlchemy.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings


# ============================================================
# CREAR EL ENGINE (MOTOR DE BASE DE DATOS)
# ============================================================
# El engine es la conexión principal a la base de datos.
# Solo necesitamos uno para toda la aplicación.

engine = create_engine(
    settings.database_url,
    # Para PostgreSQL, es buena práctica pre-crear algunas conexiones
    pool_pre_ping=True,  # Verifica que la conexión esté viva antes de usarla
    echo=settings.environment == "development"  # Muestra SQL en desarrollo
)


# ============================================================
# CREAR LA FÁBRICA DE SESIONES
# ============================================================
# SessionLocal es una "fábrica" que crea sesiones nuevas.
# Cada petición HTTP debería usar su propia sesión.

SessionLocal = sessionmaker(
    autocommit=False,  # No hacer commit automático
    autoflush=False,   # No sincronizar automáticamente con la BD
    bind=engine        # Conectar al engine que creamos
)


# ============================================================
# BASE PARA MODELOS
# ============================================================
# Todos nuestros modelos heredarán de esta clase Base.
# SQLAlchemy usa esta base para saber qué tablas crear.

Base = declarative_base()


# ============================================================
# FUNCIÓN PARA OBTENER SESIÓN
# ============================================================
# Esta función se usa como "dependencia" en FastAPI.
# Cada endpoint que necesite la BD usará esto.

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()